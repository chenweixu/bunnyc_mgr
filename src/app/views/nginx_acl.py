from app import app
from app import work_log
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.services.nginx import NginxManager
from app.main.nginx_acl import Nginx_Acl


@app.route("/api/v3/nginx", methods=["POST"])
def v3_nginx():
    work_log.info(str(request.path))
    work_log.info("request service interface, ip: %s " % (request.remote_addr))
    work_log.debug(str(request.json))
    try:
        if request.json.get("obj") != "dmz_nginx":
            return "", 404
    except Exception as e:
        return "", 404

    try:
        task = request.json.get("task")
        iplist = request.json.get("ip")

        if task in ["lock", "unlock", "clearlock", "showlock"]:
            info = Nginx_Acl()
            data = info.run_task(iplist, task)
            if task == "showlock":
                data = {
                    "ip": data.get("redata")
                }
            work_log.info('return: '+str(data))
            return jsonify(data)
        else:
            return jsonify({"redata": "req format error", "recode": 1})
    except Exception as e:
        work_log.error(str(e))
        return jsonify({"redata": "run error", "recode": 2})
