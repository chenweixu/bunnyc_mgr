from app.main.mylog import My_log
from app.main.networkmanager import NetworkManager
from app.main.hostshell import HostBaseCmd
from app.main.servicemanager import NginxManager
from app.main.servicemanager import WeblogicManager
from app.main.memcached import Memcached
from app.main.web import CheckWebInterface

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class Service(object):
    """docstring for Service"""
    def __init__(self):
        super(Service, self).__init__()

    def check_url(url):
        if not url:
            work_log.error("args error")
            return 404
        work_log.info("checkweburl: " + str(url))
        try:
            info = CheckWebInterface()
            recode = info.get_url_status_code(url, timeout=2)
            work_log.debug(str(recode))
            return recode
        except Exception as e:
            work_log.error("checkweburl error")
            work_log.error(str(e))
            return 498


    def run_task(data):
        work_log.debug(str(data))
        unit = data.get("unit")
        task = data.get("task")

        if unit == "nginx":
            if task in ["lock", "ulock", "showlock"]:
                lock_ip = request.json.get("lock_ip")
                work_log.info("nginx task: %s :  ip: %s" % (str(task), str(lock_ip)))
                info = NginxManager()
                data = info.lock_ip(lock_ip, task)
                return data
            elif request.json.get("server"):
                server = request.json.get("server")
                work_log.debug("nginx task: %s, webserver: %s " % (str(task),str(webserver))
                info = NginxManager()
                data = info.nginx_task(server, task)
                return data
            else:
                work_log.error("recode: 9999, req format error")
                return {"recode": 9999, "data": "req format error"}

        if unit == 'memcached':
            info = MemcachedManager()
            if task in ["start", "stop", "reboot"]:
                data = info.run_task(data)
                return data
            elif task in ["link_sum", "get", "set", "cleardata"]:
                data = info.data_task(request.json)
                return data
            else:
                return jsonify({"recode": 99, "redata": "format error"})

        if unit == 'weblogic':
            work_log.debug("---------------- weblogic task start ----------------")
            info = WeblogicManager()

            if task == "start_group" or task == "stop_group":
                group_number = data.get("group_number")
                work_log.debug(group_number)
                data = info.run_task_group(task, group_number)

            elif task in ("start", "stop", "show_access_log", "show_error_log"):
                service_number = request.args.get("service_number")
                hosts = request.args.get("hosts")
                work_log.debug(service_number)
                data = info.run_task(hosts, task, service_number)
            else:
                data = {"recode": 9, "redata": "参数错误"}
            work_log.info(data)
            work_log.debug("---------------- weblogic task end ----------------")
            return data
