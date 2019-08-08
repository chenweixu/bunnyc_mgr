import re
from app.main.conf import conf_data
from app.main.server.hostbase import HostBaseCmd
from app.main.server.hostgroup import HostGroupCmd
from app.utils.NetCache import NetCache
from app import work_log

class NginxManager(object):
    """docstring for NginxManager"""

    def __init__(self):
        super(NginxManager, self).__init__()
        self.user = conf_data("user_info", "default_user")
        service_script = conf_data("service_info", "local_service_script")
        self.start_cmd = " ".join([service_script, "nginx", "start"])
        self.stop_cmd = " ".join([service_script, "nginx", "stop"])
        self.reload_cmd = " ".join([service_script, "nginx", "reload"])
        self.nginx_access_log = conf_data("service_info", "nginx", "nginx_access_log")
        self.nginx_error_log = conf_data("service_info", "nginx", "nginx_error_log")
        self.master_conf = conf_data("service_info", "nginx", "master_conf")
        self.deny_conf = conf_data("service_info", "nginx", "deny_conf")

    def __ssh_cmd(self, host, cmd):
        work_log.info("exec remote cmd nginx")
        work_log.info(cmd)
        a = HostBaseCmd(host, self.user)
        status, data = a.ssh_cmd(cmd, stdout=True)
        return status, data

    def showlock(self):
        cmd = f"grep http_x_forwarded_for {self.deny_conf}"
        ip = conf_data("service_info", "nginx", "dmz")[0]
        try:
            recode, data = self.__ssh_cmd(ip, cmd)
            lock_ip = re.compile("\d+.\d+.\d+.\d+").findall(data)

            try:
                lock_ip.remove("1.1.1.254")
            except ValueError:
                pass

            work_log.debug("showlockip: " + str(lock_ip))
            return {"recode": 0, "redata": lock_ip}
        except Exception as e:
            work_log.error("show lock ip error")
            work_log.error(str(e))
            return {"recode": 2, "redata": str(e)}

    def get_nginx_lock_unlock_cmd(self, iplist, task, multiple=None):
        data = []
        cache = NetCache()
        lock_list = cache.setSmembers()
        if task == "clearlock":
            cache.setDel()
            cmd = f"""sed -i '/http_x_forwarded_for/s/".*"/"1.1.1.254"/' {self.deny_conf}"""
            data.append(cmd)
            data.append(self.reload_cmd)
            return data

        if task not in ["lock", "unlock"]:
            raise ValueError
        if multiple:
            for ip in iplist:
                work_log.debug(f'{ip}')
                if task == "lock" and ip not in lock_list:
                    cmd = f"""sed -i '/http_x_forwarded_for/s/")/|{ip}")/' {self.deny_conf}"""
                    data.append(cmd)
                    cache.setAdd(ip)
                elif task == "unlock" and ip in lock_list:
                    cmd = f"""sed -i '/http_x_forwarded_for/s/|{ip}//' {self.deny_conf}"""
                    data.append(cmd)
                    cache.setRemove(ip)
                else:
                    work_log.info(f'not task: {task} {ip} in or in lock_list')
        elif not multiple:
            # iplist 实际上为单个IP字符串
            if task == "lock" and iplist not in lock_list:
                cmd = f"""sed -i '/http_x_forwarded_for/s/")/|{iplist}")/' {self.deny_conf}"""
                data.append(cmd)
                cache.setAdd(iplist)
            elif task == "unlock" and iplist in lock_list:
                cmd = f"""sed -i '/http_x_forwarded_for/s/|{iplist}//' {self.deny_conf}"""
                data.append(cmd)
                cache.setRemove(iplist)
            elif task == "unlock" and iplist not in lock_list:
                work_log.info(f'not task: {task} {iplist} not in lock_list')
                return "IP地址未在锁定列表"
            elif task == "lock" and iplist in lock_list:
                work_log.info(f'not task: {task} {iplist} in lock_list')
                return "IP地址已经在锁定列表"
            else:
                pass
        if not data:
            # 需屏蔽的IP都已屏蔽，需解锁的IP并未屏蔽
            return data
        data.append(self.reload_cmd)
        return data

    def lock_ip(self, ip, task, multiple=None):
        if task == "showlock":
            cache = NetCache()
            lock_list = cache.setSmembers()
            work_log.info(f'task: showlock {lock_list}')
            return {"redata": list(lock_list), "recode": 0}

        if multiple:
            cmdlist = self.get_nginx_lock_unlock_cmd(ip, task, multiple=True)
        else:
            cmdlist = self.get_nginx_lock_unlock_cmd(ip, task)
        if not isinstance(cmdlist,list):
            return {"redata": cmdlist, "recode": 9}

        work_log.debug(f'{cmdlist}')
        hosts = conf_data("service_info", "nginx", "dmz")
        info = HostGroupCmd(self.user, hosts)
        try:
            for i in cmdlist:
                work_log.info(f'nginx lock task, exec: {i}')
                info.run(i)
                work_log.debug('--------------------------')
            work_log.debug('lock task all run success')
            return {"redata": "success", "recode": 0}
        except Exception as e:
            work_log.error(str(e))
            return {"recode": 2, "redata": "remote run error"}


    def Shield(self, zone, ip, port, cancel=None):
        hosts = conf_data("service_info", "nginx", zone)
        if not cancel and port != "all":
            # 屏蔽某个服务
            cmd = f'sed -i "/{ip}:{port}/s/server/#server/g" {self.master_conf}'
        elif not cancel and port == "all":
            # 屏蔽某个主机
            cmd = f'sed -i "/{ip}/s/server/#server/g" {self.master_conf}'
        elif cancel and port != "all":
            # 解除某个服务的屏蔽
            cmd = f'sed -i "/{ip}:{port}/s/#//g" {self.master_conf}'
        elif cancel and port == "all":
            cmd = f'sed -i "/{ip}/s/#//g" {self.master_conf}'
            # 解除某个主机的屏蔽

        info = HostGroupCmd(self.user, hosts)
        try:
            info.run(cmd)
            info.run(self.reload_cmd)
            return {"recode": 0, "redata": "success"}
        except Exception as e:
            work_log.error(str(e))
            return {"recode": 2, "redata": "remote run error"}

    def nginx_task(self, ip, task):
        work_log.debug("nginx_task task: " + str(task))
        if task == "start":
            recode, data = self.__ssh_cmd(ip, self.start_cmd)
        elif task == "stop":
            recode, data = self.__ssh_cmd(ip, self.stop_cmd)
        elif task == "reload":
            recode, data = self.__ssh_cmd(ip, self.reload_cmd)
        elif task == "restart":
            self.__ssh_cmd(ip, self.stop_cmd)
            recode, data = self.__ssh_cmd(ip, self.start_cmd)
        elif task == "show_access_log":
            cmd = "tail -n 200 " + self.nginx_access_log
            recode, data = self.__ssh_cmd(ip, cmd)
        elif task == "show_error_log":
            cmd = "tail -n 200 " + self.nginx_error_log
            recode, data = self.__ssh_cmd(ip, cmd)

        elif task == "clear_access_log":
            cmd = "> " + self.nginx_access_log
            recode, data = self.__ssh_cmd(ip, cmd)
        else:
            return {"recode": 2, "redata": "not found task"}

        if not data:
            data = "sucesse"

        newdata = {"redata": data, "recode": recode}
        return newdata
