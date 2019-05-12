from app import app
from flask import request
from flask import jsonify

from app.utils.mylog import My_log
from app.utils.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.host import HostTask

logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()


@app.route("/api/v2/host", methods=["GET", "POST"])
def v2_host():
    work_log.debug(str(request.path))
    work_log.info("request host interface ip: %s" % (request.remote_addr))

    if request.method == "GET":
        return "", 404
    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == "host":
                info = HostTask(request.json.get("content"))
                data = info.run()
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("host run error")
            work_log.error(str(e))
            return jsonify({"recode": 9, "redata": str(e)})
    else:
        return "", 404
