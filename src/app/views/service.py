from app import app
from app import work_log
from flask import request
from flask import jsonify
from app.utils.myencrypt import create_key, verify_key
from app.main.service import Service
from app.main.services.nginx import NginxManager


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

@app.route("/api/v3/nginx", methods=["POST"])
def v3_nginx():
    work_log.info(str(request.path))
    work_log.info("request service interface, ip: %s " % (request.remote_addr))

    try:
        if request.json.get("obj") != "dmz_nginx":
            return "", 404
    except Exception as e:
        return "", 404

    try:
        task = request.json.get("task")
        iplist = request.json.get("ip")

        if task in ["lock", "unlock", "clearlock", "showlock"]:
            info = NginxManager()
            data = info.lock_ip(iplist, task, multiple=True)
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
