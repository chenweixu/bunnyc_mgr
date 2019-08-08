from app.main.conf import conf_data
from app.main.server.hostgroup import HostGroupCmd
from app.utils.NetCache import NetCache
from app import work_log


class Nginx_Acl(object):
    """docstring for Nginx_Acl"""

    def __init__(self):
        super(Nginx_Acl, self).__init__()
        self.user = conf_data("user_info", "default_user")
        service_script = conf_data("service_info", "local_service_script")
        self.reload_cmd = " ".join([service_script, "nginx", "reload"])
        self.deny_conf = conf_data("service_info", "nginx", "deny_conf")
        self.cache = NetCache()

    def run_task_list(self, cmdlist):
        cmdlist.append(self.reload_cmd)  # add reload
        work_log.debug(f"{cmdlist}")
        hosts = conf_data("service_info", "nginx", "dmz")
        try:
            info = HostGroupCmd(hosts, self.user)
            for i in cmdlist:
                work_log.info(f"nginx lock task, exec: {i}")
                info.run(i)
                work_log.debug("--------------------------")
            work_log.debug("lock task all run success")
            return {"redata": "success", "recode": 0}
        except Exception as e:
            work_log.error(str(e))
            return {"recode": 2, "redata": "nginx server error"}

    def clear_lock(self):
        data = []
        self.cache.setDel()  # 清空redis缓存
        cmd = f"""sed -i '/http_x_forwarded_for/s/".*"/"1.1.1.254"/' {self.deny_conf}"""
        data.append(cmd)
        data.append(self.reload_cmd)
        return self.run_task_list(data)

    def show_lock(self):
        lock_list = self.cache.setSmembers()  # 获取集合全部数据
        work_log.info(f"task: showlock {lock_list}")
        return {"redata": list(lock_list), "recode": 0}

    def lock_ip(self, iplist):
        data = []
        lock_list = self.cache.setSmembers()
        for ip in iplist:
            work_log.debug(f"{ip}")
            if ip not in lock_list:
                cmd = (
                    f"""sed -i '/http_x_forwarded_for/s/")/|{ip}")/' {self.deny_conf}"""
                )
                data.append(cmd)
                self.cache.setAdd(ip)
            else:
                work_log.error(f"lock: {ip} in lock_list")
        if not data:
            # 需解锁的IP并未屏蔽
            # 多个IP中部分存在的情况暂缓
            return {"redata": str(iplist) + " IP地址已经在锁定列表", "recode": 1}
        return self.run_task_list(data)

    def unlock_ip(self, iplist):
        data = []
        lock_list = self.cache.setSmembers()
        for ip in iplist:
            work_log.debug(f"{ip}")
            if ip in lock_list:
                cmd = f"""sed -i '/http_x_forwarded_for/s/|{ip}//' {self.deny_conf}"""
                data.append(cmd)
                self.cache.setRemove(ip)
            else:
                work_log.error(f"unlock: {ip} no in lock_list")
        if not data:
            # 需解锁的IP并未屏蔽
            return {"redata": str(iplist) + " IP地址未在锁定列表", "recode": 1}
        return self.run_task_list(data)

    def run_task(self, iplist, task):
        """锁定/解锁/查看锁/清除锁
        """
        if task == "showlock":
            return self.show_lock()
        elif task == "clearlock":
            return self.clear_lock()
        elif task == "lock":
            return self.lock_ip(iplist)
        elif task == "unlock":
            return self.unlock_ip(iplist)
        else:
            return {"redata": "task error", "recode": 9}
