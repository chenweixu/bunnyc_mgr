import re
from app.main.conf import conf_data
from app.utils.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.hostshell import HostGroupCmd

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


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
        cmd = f"grep clientRealIp {self.deny_conf}"
        ip = conf_data("service_info", "nginx", "dmz")[0]
        try:
            recode, data = self.__ssh_cmd(ip, cmd)
            lock_ip = re.compile("\d+.\d+.\d+.\d+").findall(data)
            work_log.debug("showlockip: " + str(lock_ip))
            return {"recode": 0, "redata": lock_ip}
        except Exception as e:
            work_log.error("show lock ip error")
            work_log.error(str(e))
            return {"recode": 2, "redata": str(e)}

    def lock_ip(self, ip, task):
        if task == "lock":
            cmd = f"""sed -i '/clientRealIp/s/")/|{ip}")/' {self.deny_conf}"""
        elif task == "ulock":
            cmd = f"""sed -i '/clientRealIp/s/|{ip}//' {self.deny_conf}"""
        else:
            return {"recode": 1, "redata": "req format error"}

        hosts = conf_data("service_info", "nginx", "dmz")

        info = HostGroupCmd(self.user, hosts)
        try:
            data1 = info.run(cmd)
            data2 = info.run(self.reload_cmd)
            work_log.info("lock_ip run info: %s" % data1)
            if max(data1) == 0 and max(data2) == 0:
                return {"redata": "all yes", "recode": 0}
            else:
                return {"redata": "error", "recode": 2}
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
