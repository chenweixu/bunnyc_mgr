import re
from app import work_log
from app.main.conf import conf_data
from app.main.services.web import CheckWebInterface
from app.main.services.memcached import MemcachedManagerSingle
from app.main.services.memcached import MemcachedManagerGroup
from app.main.services.memcached import MemcachedDataSingle
from app.main.services.nginx import NginxManager
from app.main.nginx_acl import Nginx_Acl
from app.main.services.weblogic import WeblogicManagerSingle
from app.main.services.weblogic import WeblogicManagerGroup
from app.main.services.weblogic import WeblogicManagerCheck


class Service(object):
    """docstring for Service"""

    def __init__(self):
        super(Service, self).__init__()

    def check_url(self, url):
        work_log.info("checkweburl: " + str(url))
        try:
            info = CheckWebInterface()
            recode = info.get_url_status_code(url, timeout=2)
            work_log.debug(str(recode))
            if recode == 200:
                return {"recode": 0, "redata": "success 成功"}
            else:
                return {"recode": recode, "redata": "error"}
        except Exception as e:
            work_log.error("checkweburl error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "server error"}


    def weblogic(self, data):
        task = data.get("task")
        types = data.get("types")
        work_log.debug("---------------- weblogic task start ----------------")

        if types == 'single':
            work_log.debug(str(data))
            server = data.get("server")
            port = data.get("port")
            info = WeblogicManagerSingle(server, port)
            return info.run_task(task)

        elif types == 'group':
            group = data.get("group")
            work_log.debug(group)

            # 全部服务检查
            if group == "all" and task == "check":
                work_log.debug(f"wg check all service")
                info = WeblogicManagerCheck()
                return info.check_all_weblogic_interface()

            if group not in conf_data("app_group"):
                work_log.debug(f"weblogic grou not find")
                return {"recode": 9, "redata": "参数错误"}

            if task == "check":
                work_log.debug(f"wg check group: {group}")
                info = WeblogicManagerCheck()
                return info.check_group_weblogic_interface(group)
            elif task in ["start", "stop"]:
                work_log.debug(f"wg group: {task} {group}")
                info = WeblogicManagerGroup(group)
                return info.run_task_group(task)
            else:
                work_log.debug(f"wg check args error")
                return {"recode": 9, "redata": "参数错误"}
        else:
            work_log.debug(f"weblogic types args error")
            return {"recode": 9, "redata": "参数错误"}


    def memcached(self, data):
        types = data.get("types")
        task = data.get("task")

        if types == 'single':
            server = data.get("server")
            port = data.get("port")
            if task in ["start", "stop"]:
                info = MemcachedManagerSingle(server, port)
                return info.run_task(task)

        if types == 'group':
            group = data.get("group")
            if group not in conf_data("mc_group"):
                work_log.debug(f"memcached grou not find")
                return {"recode": 9, "redata": "参数错误-group错误"}

            if task in ["start", "stop"]:
                info = MemcachedManagerGroup(group)
                return info.run_task(task)

            return {"recode": 1, "redata": "format error"}
        return {"recode": 1, "redata": "format error"}

        # try:

            # elif task in []:
            #     info = MemcachedDataSingle(server, port)
            #     return info.run_task(task)

            # elif task in ["get", "set", "cleardata", "link_sum"]:
            #     info = MemcachedDataSingle(data.get("server"), data.get("port"))
            #     if task == "get":
            #         return info.get(data.get("key"))
            #     elif task == "set":
            #         return info.set(data.get("key"), data.get("value"))
            #     elif task == "cleardata":
            #         return info.clear_data()
            #     elif task == "link_sum":
            #         return info.showstatus("curr_connections")
            # else:

        # except Exception as e:
        #     work_log.error(str(e))
        #     return {"recode": 2, "redata": "run error"}


    def nginx_lock(self,data):
        task = data.get('task')
        ip = data.get("ip")
        if not isinstance(ip, list):
            iplist = []
            iplist.append(ip)
        else:
            iplist = ip

        info = Nginx_Acl()

        # if ip not in re.compile("\d+.\d+.\d+.\d+").findall(ip):
        #     return {"recode": 2, "redata": "req format error"}
        # 暂时停止IP地址校验，因为还没有考虑ipv6

        if task == 'lock':
            work_log.info(f"nginx task: lock, ip: {iplist}")
            return info.lock_ip(iplist)

        elif task == 'unlock':
            work_log.info(f"nginx task: unlock, ip: {iplist}")
            return info.unlock_ip(iplist)

        elif task == "showlock":
            work_log.info("nginx task: showlock")
            return info.show_lock()
        elif task == "clearlock":
            work_log.info("nginx task: clearlock")
            return info.clear_lock()
        else:
            return {"redata": 'task error', "recode": 1}

    def nginx_single(self, data):
        task = data.get("task")
        info = NginxManager()

        server = data.get("server")
        work_log.debug("nginx task: %s, server: %s " % (str(task), str(server)))
        data = info.nginx_task(server, task)
        return data

    def nginx_shield(self, data):
        # "shield", "cancelShield"
        # 屏蔽/解除屏蔽-后台应用服务
        ip = data.get("ip")
        port = data.get("port")
        zone = data.get("zone")
        task = data.get("task")
        info = NginxManager()
        work_log.info(
            f"nginx task: {task}, zone: {zone} ip: {ip}, port: {port}"
        )
        if task == "shield":
            return info.Shield(zone, ip, port)
        elif task == "cancelShield":
            return info.Shield(zone, ip, port, cancel=True)
        else:
            return {"recode": 1, "redata": "req format task error"}

    def nginx(self, data):
        try:
            types = data.get("types")
            if types == 'lock':
                return self.nginx_lock(data)
            if types == 'single':
                return self.nginx_single(data)
            if types == 'shield':
                return self.nginx_shield(data)
            else:
                work_log.error("recode: 1, req format error")
                return {"recode": 1, "redata": "req format error"}
        except Exception as e:
            work_log.error("nginx task error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "server run error"}

    def run_task(self, data):
        work_log.debug(str(data))
        unit = data.get("unit")

        if unit == "nginx":
            return self.nginx(data)
        if unit == "memcached":
            return self.memcached(data)
        if unit == "weblogic":
            return self.weblogic(data)
