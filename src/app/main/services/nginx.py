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
        self.upstream_conf = conf_data("service_info", "nginx", "upstream_conf")

    def __ssh_cmd(self, host, cmd):
        work_log.info("exec remote cmd nginx")
        work_log.info(cmd)
        a = HostBaseCmd(host, self.user)
        status, data = a.ssh_cmd(cmd, stdout=True)
        return status, data

    def Shield(self, zone, ip, port, cancel=None):
        hosts = conf_data("service_info", "nginx", zone)
        if not cancel and port != "all":
            # 屏蔽某个服务
            cmd = f'sed -i "/{ip}:{port}/s/server/#server/g" {self.upstream_conf}'
        elif not cancel and port == "all":
            # 屏蔽某个主机
            cmd = f'sed -i "/{ip}/s/server/#server/g" {self.upstream_conf}'
        elif cancel and port != "all":
            # 解除某个服务的屏蔽
            # 遗留：配置本行末的注释会被影响
            # 如果有多个#，则每次取消一个
            cmd = f'sed -i "/{ip}:{port}/s/#//" {self.upstream_conf}'
        elif cancel and port == "all":
            cmd = f'sed -i "/{ip}/s/#//g" {self.upstream_conf}'
            # 解除某个主机的屏蔽

        info = HostGroupCmd(hosts, self.user)
        try:
            info.run_cmd_task(cmd)
            info.run_cmd_task(self.reload_cmd)
            # 没有报错就算成功了，暂时忽略了多个主机个别错误的情况
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
