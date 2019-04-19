from app.utils.mylog import My_log
from app.main.conf import conf_data
from app.main.services.web import CheckWebInterface
from app.main.services.memcached import MemcachedManagerSingle
from app.main.services.memcached import MemcachedDataManager
from app.main.services.nginx import NginxManager
from app.main.services.weblogic import WeblogicManagerSingle
from app.main.services.weblogic import WeblogicManagerGroup
from app.main.services.weblogic import WeblogicManagerCheck


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
            if data.get("server"):
                server = data.get("server")
                work_log.debug("nginx task: %s, server: %s " % (str(task), str(server)))
                info = NginxManager()
                data = info.nginx_task(server, task)
                return data

            elif task in ["lock", "ulock"]:
                ip = data.get("ip")
                work_log.info("nginx task: %s :  ip: %s" % (str(task), str(ip)))
                info = NginxManager()
                data = info.lock_ip(ip, task)
                return data
            elif task == "showlock":
                work_log.info("nginx task: showlock")
                info = NginxManager()
                data = info.showlock()
                return data
            else:
                work_log.error("recode: 1, req format error")
                return {"recode": 1, "redata": "req format error"}

        if unit == "memcached":
            try:
                if task in ["start", "stop", "reboot"]:
                    info = MemcachedManagerSingle(data.get("server"), data.get("port"))
                    return info.run_task(task)
                elif task in ["get", "set", "cleardata", "link_sum"]:
                    info = MemcachedDataManager(data.get("server"), data.get("port"))
                    if task == "get":
                        return info.get(data.get("key"))
                    elif task == "set":
                        return info.set(data.get("key"), data.get("value"))
                    elif task == "cleardata":
                        return info.clear_data()
                    elif task == "link_sum":
                        return info.showstatus("curr_connections")
                else:
                    return {"recode": 1, "redata": "format error"}
            except Exception as e:
                work_log.error(str(e))
                return {"recode": 2, "redata": "run error"}

        if unit == "weblogic":
            work_log.debug("---------------- weblogic task start ----------------")
            # info = WeblogicManager()

            if data.get("group"):
                group = data.get("group")
                work_log.debug(group)
                info = WeblogicManagerGroup(group)
                data = info.run_task_group(task)

            elif data.get("server"):
                work_log.debug(str(data))
                server = data.get("server")
                port = data.get("port")
                info = WeblogicManagerSingle(server, port)
                data = info.run_task(task)
            else:
                data = {"recode": 9, "redata": "参数错误"}
            work_log.info(data)
            work_log.debug("---------------- weblogic task end ----------------")
            return data
