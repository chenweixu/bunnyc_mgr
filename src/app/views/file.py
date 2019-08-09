import os

from app import app
from flask import request
from flask import jsonify
from app.main.conf import conf_data
from app.utils.myencrypt import create_key, verify_key
from app.main.file_upload_down import DownRemoteFile, UpDownFile
from flask import send_file, send_from_directory
from app import work_log

@app.route("/api/v2/downfile/<file_name>", methods=["GET"])
def v2_downfile(file_name):
    '''从服务器自身的临时目录下载文件'''
    work_log.debug("---------------")
    work_log.debug(str(request.path))
    work_log.info("request host interface ip: %s" % (request.remote_addr))

    if request.method == "GET":
        tmp_dir = conf_data("work_tmp_dir")
        return send_from_directory(tmp_dir, file_name, as_attachment=True)


@app.route("/api/v2/downfile", methods=["POST"])
def v2_down():
    '''原理：从指定服务器上下载文件到临时目录，再返回一个文件的get下载路径'''
    work_log.debug("---------------")
    work_log.debug(str(request.path))
    work_log.info("request host interface ip: %s" % (request.remote_addr))

    try:
        key = request.json.get("key")
        if not verify_key(key) and request.json.get("obj") != "file":
            work_log.error("req verify_key or obj error")
            return "", 404
    except Exception as e:
        work_log.error(str(e))
        work_log.error("req verify_key or obj error")
        return "", 404

    info = DownRemoteFile(request.json.get("content"))
    data = info.down()
    return jsonify(data)


@app.route("/api/v2/upload", methods=["POST"])
def v2_upload():
    work_log.debug(str(request.path))
    work_log.info("request host interface ip: %s" % (request.remote_addr))

    try:
        file = request.files["file"]
        ip = request.form["ip"]
        destdir = request.form["dir"]
        user = request.form["user"]
        if not ip or not destdir:
            return "", 404

        work_log.info(
            f"upload file, ip: {ip}, filename: {file.filename}, dest: {destdir}, user: {user}"
        )
        tmp_dir = conf_data("work_tmp_dir")
        local_tmp = os.path.join(tmp_dir, file.filename)
        dest = os.path.join(destdir, file.filename)
        file.save(local_tmp)  # 保存临时文件

        info = UpDownFile(ip, user)
        data = info.upload(local_tmp, dest)
        os.remove(local_tmp)  # 删除临时文件
        return jsonify(data)

    except Exception as e:
        work_log.error("upload file run error")
        work_log.error(str(e))
        return jsonify({"recode": 9, "redata": str(e)})
    else:
        return "", 200
