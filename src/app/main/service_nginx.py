import re
from app.main.conf import conf_data
from app.main.util.mylog import My_log
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

    def __ssh_cmd(self, host, cmd):
        a = HostBaseCmd(host, self.user)
        status, data = a.ssh_cmd(cmd, stdout=True)
        return status, data

    def showlock(self):
        cmd = "grep clientRealIp /opt/nginx/conf/deny_ip.conf"
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
            cmd1 = (
                """sed -i '/clientRealIp/s/")/|"""
                + ip
                + """")/' /opt/nginx/conf/deny_ip.conf"""
            )
        elif task == "ulock":
            cmd1 = (
                """sed -i '/clientRealIp/s/|"""
                + ip
                + """//' /opt/nginx/conf/deny_ip.conf"""
            )
        else:
            return {"recode": 1, "redata": "req format error"}

        cmd2 = "/opt/nginx/sbin/nginx -s reload"
        hosts = conf_data("service_info", "nginx", "dmz")

        info = HostGroupCmd(self.user, hosts)
        data1 = info.run(cmd1)
        data2 = info.run(cmd2)

        work_log.info("lock_ip run info: %s" % data1)
        work_log.info("lock_ip run info: %s" % data2)
        if max(data1) == 0 and max(data2) == 0:
            return {"redata": "all yes", "recode": 0}
        else:
            return {"redata": "error", "recode": 2}

    def nginx_task(self, ip, task):
        work_log.debug("nginx_task task: " + str(task))
        start_cmd = conf_data("service_info", "nginx", "start_cmd")
        stop_cmd = conf_data("service_info", "nginx", "stop_cmd")
        reload_cmd = conf_data("service_info", "nginx", "reload_cmd")
        nginx_access_log = conf_data("service_info", "nginx", "nginx_access_log")
        nginx_error_log = conf_data("service_info", "nginx", "nginx_error_log")

        if task == "start":
            recode, data = self.__ssh_cmd(ip, start_cmd)
        elif task == "stop":
            recode, data = self.__ssh_cmd(ip, stop_cmd)
        elif task == "reload":
            recode, data = self.__ssh_cmd(ip, reload_cmd)
        elif task == "restart":
            self.__ssh_cmd(ip, stop_cmd)
            recode, data = self.__ssh_cmd(ip, start_cmd)
        elif task == "show_access_log":
            cmd = "tail -n 200 " + nginx_access_log
            recode, data = self.__ssh_cmd(ip, cmd)
        elif task == "show_error_log":
            cmd = "tail -n 200 " + nginx_error_log
            recode, data = self.__ssh_cmd(ip, cmd)

        elif task == "clear_access_log":
            cmd = "> " + nginx_access_log
            recode, data = self.__ssh_cmd(ip, cmd)
        else:
            return {"recode": 2, "redata": "not found task"}

        if not data:
            data = "sucesse"

        newdata = {"redata": data, "recode": recode}
        return newdata
