from app import app
from flask import request
from flask import jsonify

from app.utils.mylog import My_log
from app.utils.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.network import NetWork
from app.main.service import Service

logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()


@app.route("/api/v2/network", methods=["GET", "POST"])
def v2_network():
    work_log.debug(str(request.path))
    work_log.debug("request network interface, ip: %s " % (request.remote_addr))
    if request.method == "GET":
        ipaddr = request.args.get("ip")
        url = request.args.get("url")

        if ipaddr:
            info = NetWork()
            data = info.ping(ipaddr)
            return jsonify(data)
        elif url:
            info = Service()
            data = info.check_url(url)
            return jsonify(data)
        else:
            work_log.error(str("req format error"))
            return "", 404

    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == "network":
                info = NetWork()
                data = info.run_task(request.json.get("content"))
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("req error")
            work_log.error(str(e))
            return "", 404
    else:
        return "", 404
