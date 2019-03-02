from app import app
from flask import request
from flask import jsonify
from app.main.util.mylog import My_log
from app.main.util.myencrypt import create_key, verify_key
from app.main.conf import conf_data
from app.main.sms_tools import Sms_tools
from app.main.host import HostTask
from app.main.network import NetWork
from app.main.service import Service
from app.main.monitor_data import MonitorTask

logfile = conf_data("work_log")
log_evel = conf_data("log_evel")
work_log = My_log(logfile, log_evel).get_log()


@app.route("/")
def index():
    # data = app.config['RUN_MODEL']
    data = 'Hello cwx!'
    return str(data), 200


@app.route('/api/v2/sms', methods=['GET', 'POST'])
def sms_send():
    if request.method == 'GET':
        work_log.debug(str(request.path))

        phone = request.args.get('phone')
        if not phone:
            return 'error', 404
        else:
            body = request.args.get('body')
            work_log.info(str(body))

            phone_list = phone.split(',')
            work_log.debug(str(phone_list))

            sms = Sms_tools()

            data = sms.send_mess(phone_list, body)
            if data == 1:
                work_log.error('link sms webservice interface error')
                return '', 510
            elif data == 2:
                work_log.error('webservice interface args error')
                return '', 511
            else:
                work_log.debug(str('sms_send yes-------------'))
                return '', 200
    else:
        return 'error', 404

@app.route("/api/v2/host", methods=["GET", "POST"])
def v2_host():
    work_log.debug(str(request.path))
    work_log.info("request host interface ip: %s" % (request.remote_addr))

    if request.method == "GET":
        return "", 404
    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == 'host':
                info = HostTask(request.json.get('content'))
                data = info.run()
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("host run error")
            work_log.error(str(e))
            return "", 404
    else:
        return "", 404


@app.route("/api/v2/monitor", methods=["GET", "POST"])
def v2_monitor():
    work_log.debug(str(request.path))
    work_log.info("request MonitorTask interface ip: %s" % (request.remote_addr))
    if request.method == "GET":
        return "", 404
    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == 'host':
                info = MonitorTask(request.json.get('content'))
                data = info.run()
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("req format error")
            work_log.error(str(e))
            return "", 404
    else:
        return "", 404


@app.route("/api/v2/network", methods=["GET", "POST"])
def v2_network():
    work_log.debug(str(request.path))
    work_log.debug("request network interface, ip: %s " % (request.remote_addr))
    if request.method == "GET":
        ipaddr = request.args.get("host")
        if not ipaddr:
            work_log.error(str("req format error"))
            return "error", 404
        else:
            info = NetWork()
            data = info.ping(ipaddr)
            return jsonify(data)

    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == 'network':
                info = NetWork()
                data = info.run_task(request.json.get('content'))
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


@app.route("/api/v2/service", methods=["GET", "POST"])
def v2_service():
    work_log.debug(str(request.path))
    work_log.debug("request service interface, ip: %s " % (request.remote_addr))

    if request.method == "GET":
        task = request.args.get("task")
        if task == 'checkurl':
            url = request.args.get("url")
            info = Service()
            recode = info.check_url(url)
            return '', recode
        else:
            work_log.debug('checkurl req format error')
            return '', 401
    elif request.method == "POST":
        try:
            key = request.json.get("key")
            if verify_key(key) and request.json.get("obj") == 'service':
                info = Service()
                data = info.run_task(request.json.get('content'))
                return jsonify(data)
            else:
                work_log.error("req verify_key or obj error")
                return "", 404
        except Exception as e:
            work_log.error("req format error")
            work_log.error(str(e))
            return "", 404
