from app.main.util.mylog import My_log
from app.main.networkmanager import NetworkManager
from app.main.hostshell import HostBaseCmd
from app.main.servicemanager import NginxManager
from app.main.servicemanager import WeblogicManager
from app.main.util.memcached import Memcached
from app.main.web import CheckWebInterface
from app.main.conf import conf_data

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class Service(object):
    """docstring for Service"""
    def __init__(self):
        super(Service, self).__init__()

    def check_url(self, url):
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

    def run_task(self, data):
        work_log.debug(str(data))
        unit = data.get("unit")
        task = data.get("task")

        if unit == "nginx":
            if task in ["lock", "ulock", "showlock"]:
                lock_ip = data.get("lock_ip")
                work_log.info("nginx task: %s :  ip: %s" % (str(task), str(lock_ip)))
                info = NginxManager()
                data = info.lock_ip(lock_ip, task)
                return data
            elif data.get("server"):
                server = data.get("server")
                work_log.debug("nginx task: %s, server: %s " % (str(task),str(server)))
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
                data = info.data_task(data)
                return data
            else:
                return {"recode": 99, "redata": "format error"}

        if unit == 'weblogic':
            work_log.debug("---------------- weblogic task start ----------------")
            info = WeblogicManager()
            if data.get('group'):
                group = data.get("group")
                work_log.debug(group)
                data = info.run_task_group(task, group)

            elif data.get("server"):
                server = data.get("server")
                hosts = data.get("hosts")
                work_log.debug(server)
                data = info.run_task(hosts, task, server)
            else:
                data = {"recode": 9, "redata": "参数错误"}
            work_log.info(data)
            work_log.debug("---------------- weblogic task end ----------------")
            return data
