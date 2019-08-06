from app import app
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.host import HostTask
from app import work_log

@app.route("/api/v2/host", methods=["POST"])
def v2_host():
    work_log.debug(str(request.path))
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

