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


    def get_run_data(self, data):
        total = 0
        count = len(data)
        for i in data:
            total += i[0]
        if total == 0:
            # 全部成功
            return {'recode': 0, 'redata': 'success'}
        if total < 2*count:
            # 部分错误
            return {'recode': 8, 'redata': data}
        if total == 2*count:
            # 全部错误
            return {'recode': 9, 'redata': data}

    def run_task_list(self, cmdlist):
        cmdlist.append(self.reload_cmd)  # add reload
        work_log.debug(f"{cmdlist}")
        hosts = conf_data("service_info", "nginx", "dmz")
        try:
            info = HostGroupCmd(hosts, self.user)
            for i in cmdlist:
                work_log.info(f"nginx lock task, exec: {i}")
                run_data_list = info.run_cmd_task(i)
                work_log.info(str(run_data_list))
                work_log.debug("--------------------------")
            # 遗留问题，此处只处理了最后一个返回结果
            return self.get_run_data(run_data_list)
            work_log.debug("lock task all run")
            # return {"redata": "success", "recode": 0}
        except Exception as e:
            work_log.error(str(e))
            return {"recode": 2, "redata": "nginx server error"}

    def clear_lock(self):
        data = []
        cmd = f"""sed -i '/http_x_forwarded_for/s/".*"/"1.1.1.254"/' {self.deny_conf}"""
        data.append(cmd)
        data.append(self.reload_cmd)
        rundata = self.run_task_list(data)
        if rundata.get('recode') == 0:
            self.cache.setDel()  # 清空redis缓存
            work_log.info('cache clear')
        elif rundata.get('recode') == 8:
            self.cache.setDel()
            work_log.info('任务不完全成功，仍然清除了 cache lock')
        elif rundata.get('recode') == 9:
            work_log.info('not clear all lock')
        return rundata


    def show_lock(self):
        lock_list = self.cache.setSmembers()  # 获取集合全部数据
        work_log.info(f"task: showlock {lock_list}")
        return {"redata": list(lock_list), "recode": 0}

    def lock_ip(self, iplist):
        cmdlist = []

        lock_list = self.cache.setSmembers()
        for ip in iplist:
            work_log.debug(f"{ip}")
            if ip not in lock_list:
                cmd = (
                    f"""sed -i '/http_x_forwarded_for/s/")/|{ip}")/' {self.deny_conf}"""
                )
                cmdlist.append(cmd)

            else:
                work_log.error(f"lock: {ip} in lock_list")
        if not cmdlist:
            # 需解锁的IP并未屏蔽
            # 多个IP中部分存在的情况暂缓
            return {"redata": str(iplist) + " IP地址已经在锁定列表", "recode": 1}

        rundata = self.run_task_list(cmdlist)
        if rundata.get('recode') == 0:
            self.cache.setAdd(ip)
            work_log.info('cache lock')
        elif rundata.get('recode') == 8:
            self.cache.setAdd(ip)
            work_log.info(f'server run error, yes cache +lock')
        elif rundata.get('recode') == 9:
            work_log.info(f'server run error, not cache +lock')
        return rundata


    def unlock_ip(self, iplist):
        cmdlist = []
        lock_list = self.cache.setSmembers()
        for ip in iplist:
            work_log.debug(f"{ip}")
            if ip in lock_list:
                cmd = f"""sed -i '/http_x_forwarded_for/s/|{ip}//' {self.deny_conf}"""
                cmdlist.append(cmd)
            else:
                work_log.error(f"unlock: {ip} no in lock_list")
        if not cmdlist:
            # 需解锁的IP并未屏蔽
            return {"redata": str(iplist) + " IP地址未在锁定列表", "recode": 1}

        rundata = self.run_task_list(cmdlist)
        if rundata.get('recode') == 0:
            self.cache.setRemove(ip)
            work_log.info('cache unlock')
        elif rundata.get('recode') == 8:
            self.cache.setRemove(ip)
            work_log.info('server run error, yes cache unlock')
        elif rundata.get('recode') == 9:
            work_log.info('server run error, not cache unlock')
        return rundata

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
