from app import app
from app import work_log
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.service import Service


@app.route("/api/v2/service", methods=["POST"])
def v2_service():
    work_log.debug(str(request.path))
    work_log.debug("request service interface, ip: %s " % (request.remote_addr))
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

