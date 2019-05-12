from app import app
from flask import request
from flask import jsonify

from app.utils.mylog import My_log
from app.utils.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.service import Service

logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()


@app.route("/api/v2/service", methods=["GET", "POST"])
def v2_service():
    work_log.debug(str(request.path))
    work_log.debug("request service interface, ip: %s " % (request.remote_addr))

    if request.method == "GET":
        task = request.args.get("task")
        if task == "checkurl":
            url = request.args.get("url")
            info = Service()
            recode = info.check_url(url)
            return "", recode
        else:
            work_log.debug("checkurl req format error")
            return "", 401
    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == "service":
                info = Service()
                data = info.run_task(request.json.get("content"))
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("req format error")
            work_log.error(str(e))
            return "", 404
