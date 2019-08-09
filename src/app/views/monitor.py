from app import app
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.monitor_data import MonitorTask
from app.main.cmdb import cmdb
from app import work_log


@app.route("/api/v2/monitor", methods=["POST"])
def v2_monitor():
    work_log.info("request MonitorTask interface ip: %s" % (request.remote_addr))
    try:
        key = request.json.get("key")
        if verify_key(key) and request.json.get("obj") == "monitor":
            info = MonitorTask()
            data = info.run(request.json.get("content"))
            work_log.info(str(data))
            return jsonify(data)
        else:
            work_log.error("format error")
            return "", 404
    except Exception as e:
        work_log.error(str(e))
        return jsonify({"recode": 1, "redata": "run error"})
