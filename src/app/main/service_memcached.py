import time
from app.main.conf import conf_data
from app.main.util.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.hostshell import HostGroupCmd
from app.main.util.memcached import Memcached

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class Memcached_single(object):
    """docstring for Memcached_sigle"""

    def __init__(self, ip, port):
        super(Memcached_sigle, self).__init__()
        self.ip = ip
        self.port = port
        # self.task = task
        self.user = conf_data("user_info", "default_user")
        self.pidfile = conf_data("service_info", "memcached", "pidfile")
        self.start_cmd = conf_data("service_info", "memcached", "start_cmd")
        self.stop_cmd = conf_data("service_info", "memcached", "stop_cmd")


    def _mc_ssh_cmd(self, host, cmd):
        work_log.info("_mc_ssh_cmd host: %s cmd: %s" % (host, cmd))
        try:
            ssh = HostBaseCmd(host, user=self.user)
            status = ssh.ssh_cmd(cmd)
            work_log.info("_mc_ssh_cmd exec success")
            return status
        except Exception as e:
            work_log.error("_mc_ssh_cmd Exception error")
            work_log.error(str(e))
            return 90


    def start(self):
        mc_pidfile = self.pidfile.replace("1111", str(self.port))
        cmd1 = self.start_cmd.replace("mc_port", str(self.port))
        cmd = cmd1.replace("mc_pidfile", mc_pidfile)
        work_log.debug("start_mc: %s" % cmd)
        return self._mc_ssh_cmd(self.host, cmd)

    def stop(self):
        mc_pidfile = self.pidfile.replace("1111", str(self.port))
        cmd = self.stop_cmd.replace("mc_pidfile", mc_pidfile)
        work_log.debug("stop_mc: %s" % cmd)
        return self._mc_ssh_cmd(host, cmd)

    def reboot(self):
        self.stop()
        time.sleep(1)
        self.start()

    def run(self):
        pass


class MemcachedGroup(object):
    """docstring for MemcachedGroup"""
    def __init__(self, mc_list):
        super(MemcachedGroup, self).__init__()
        self.mc_list = mc_list

    def clear_mc_group(self):
        data = []
        for i in self.mc_list:
            host = i.split()[0]
            port = i.split()[1]
            server = Memcached_data(host, port)
            status = server.clear_data()
            data.append((host, port, status))
        return data

    def start_mc_group(self):
        data = []
        for i in self.mc_list:
            host = i.split()[0]
            port = i.split()[1]
            server = Memcached_single(host, port)
            status = server.start()
            data.append((host, port, status))
        return data

    def stop_mc_group(self):
        data = []
        for i in self.mc_list:
            host = i.split()[0]
            port = i.split()[1]
            server = Memcached_single(host, port)
            status = server.stop()
            data.append((host, port, status))
        return data

    def reboot_mc_group(self):
        self.stop_mc_group(mc_list)
        time.sleep(2)
        data = self.start_mc_group(mc_list)
        return data


class MemcachedManager(object):
    """docstring for MemcachedManager"""

    def __init__(self, ip ,port):
        super(MemcachedManager, self).__init__()
        self.user = conf_data("user_info", "default_user")
        self.pidfile = conf_data("service_info", "memcached", "pidfile")
        self.start_cmd = conf_data("service_info", "memcached", "start_cmd")
        self.stop_cmd = conf_data("service_info", "memcached", "stop_cmd")
        self.ip = ip
        self.port = port

    def run_task(self, task):
        if task == 'start':
            pass
        if task == 'stop':
            pass
        if task == 'reboot':
            pass
        if task == 'start':
            pass
        if task == 'start':
            pass



    def run_task_group(self,task):
        pass

    def get_data(self, key):
        mc = Memcached(ip, int(port))
        return mc.get(key)

    def set_data(self, key, value):
        mc = Memcached(ip, int(port))
        return mc.set(key, value)

    def clear_data(self):
        try:
            mc = Memcached(ip, int(port))
            mc.flush_all()
            work_log.info(
                str("flush_all mc success, host: %s ,port: %s" % (host, str(port)))
            )
            return 0
        except Exception as e:
            work_log.error(
                str("flush_all mc error, host: %s ,port: %s" % (host, str(port)))
            )
            work_log.error(str(e))
            return 99



    # def _mc_ssh_cmd(self, host, cmd):
    #     work_log.info("_mc_ssh_cmd host: %s cmd: %s" % (host, cmd))
    #     try:
    #         ssh = HostBaseCmd(host, user=self.user)
    #         status = ssh.ssh_cmd(cmd)
    #         work_log.info("_mc_ssh_cmd exec success")
    #         return status
    #     except Exception as e:
    #         work_log.error("_mc_ssh_cmd Exception error")
    #         work_log.error(str(e))
    #         return 90

    # def _clear_mc(self, host, port):
    #     mc = Memcached(host, int(port))
    #     try:
    #         mc.flush_all()
    #         work_log.info(
    #             str("flush_all mc success, host: %s ,port: %s" % (host, str(port)))
    #         )
    #         return 0
    #     except Exception as e:
    #         work_log.error(
    #             str("flush_all mc error, host: %s ,port: %s" % (host, str(port)))
    #         )
    #         work_log.error(str(e))
    #         return 91

    # def clear_mc_group(self, mc_list):
    #     data = []
    #     for i in mc_list:
    #         host = i.split()[0]
    #         port = i.split()[1]
    #         status = self._clear_mc(host, port)
    #         data.append((host, port, status))
    #     return data

    # def start_mc(self, host, port):
    #     mc_pidfile = self.pidfile.replace("1111", str(port))
    #     cmd1 = self.start_cmd.replace("mc_port", str(port))
    #     cmd = cmd1.replace("mc_pidfile", mc_pidfile)
    #     work_log.debug("start_mc: %s" % cmd)
    #     return self._mc_ssh_cmd(host, cmd)

    # def start_mc_group(self, mc_list):
    #     data = []
    #     for i in mc_list:
    #         host = i.split()[0]
    #         port = i.split()[1]
    #         status = self.start_mc(host, port)
    #         data.append((host, port, status))
    #     return data

    # def stop_mc(self, host, port):
    #     mc_pidfile = self.pidfile.replace("1111", str(port))
    #     cmd = self.stop_cmd.replace("mc_pidfile", mc_pidfile)
    #     work_log.debug("stop_mc: %s" % cmd)
    #     return self._mc_ssh_cmd(host, cmd)

    # def stop_mc_group(self, mc_list):
    #     data = []
    #     for i in mc_list:
    #         host = i.split()[0]
    #         port = i.split()[1]
    #         status = self.stop_mc(host, port)
    #         data.append((host, port, status))
    #     return data

    # def reboot_mc_group(self, mc_list):
    #     work_log.debug("reboot mc group: " + str(mc_list))
    #     self.stop_mc_group(mc_list)
    #     time.sleep(2)
    #     data = self.start_mc_group(mc_list)
    #     return data

    def get_connections_sum(self, host, port):
        mc = Memcached(host, int(port))
        curr_connections = mc.get_connections_sum()
        work_log.info("mc link_sum: " + str(curr_connections))
        return curr_connections

    def get_mc_base_info(self, host, port):
        mc = Memcached(host, int(port))
        curr_connections = mc.get_connections_sum()
        mem_user_rate = mc.get_mem_rate()
        if curr_connections != 0:
            check_ok = 0
        else:
            check_ok = 1
        return (host, port, curr_connections, mem_user_rate, check_ok)

    def check_memcached(self, data):
        mc_data = []
        for i in data:
            host = i.split()[0]
            port = int(i.split()[1])
            txt = self.get_mc_base_info(host, port)
            mc_data.append(txt)
        return mc_data

    def run_single_task(self):
        pass

    # def run_task(self, mc_task):
    #     work_log.debug("MemcachedManager run task")
    #     work_log.debug("mc_task: " + str(mc_task))
    #     task = mc_task.get("task")
    #     mc_obj = mc_task.get("mc_addr")

    #     if mc_obj == "all":
    #         recode = 2
    #     elif mc_obj in ["dmz", "cd"]:
    #         mc_list = conf_data("service_info", "memcached", mc_obj)
    #         if task == "start":
    #             recode = self.start_mc_group(mc_list)
    #         elif task == "stop":
    #             recode = self.stop_mc_group(mc_list)
    #         elif task == "reboot":
    #             recode = self.reboot_mc_group(mc_list)
    #         else:
    #             recode = 3
    #     else:
    #         mc_addr = mc_obj.split(":")[0]
    #         mc_port = int(mc_obj.split(":")[1])
    #         if task == "start":
    #             recode = self.start_mc(mc_addr, mc_port)
    #         elif task == "stop":
    #             recode = self.stop_mc(mc_addr, mc_port)
    #         elif task == "reboot":
    #             self.stop_mc(mc_addr, mc_port)
    #             time.sleep(1)
    #             recode = self.start_mc(mc_addr, mc_port)
    #         else:
    #             recode = 3

    #     if recode == 0:
    #         return {"recode": 0, "redata": "run succsse"}
    #     elif recode == 1:
    #         return {"recode": 1, "redata": "run error"}
    #     elif recode == 2:
    #         return {"recode": 2, "redata": "暂不支持"}
    #     elif recode == 3:
    #         return {"recode": 3, "redata": "format error"}
    #     else:
    #         return {"recode": 4, "redata": "other error"}

    def data_task(self, mc_task):
        work_log.debug("MemcachedManager data run")
        work_log.debug("mc_task: " + str(mc_task))
        task = mc_task.get("task")
        mc_obj = mc_task.get("mc_addr")

        redata = "run succsse"

        if mc_obj == "all":
            return {"": 2, "redata": "暂不支持"}

        mc_addr = mc_obj.split(":")[0]
        mc_port = int(mc_obj.split(":")[1])

        if task == "link_sum":
            redata = self.get_connections_sum(mc_addr, mc_port)

        key = mc_task.get("mc_key")
        mc = Memcached(mc_addr, mc_port)

        if task == "get":
            body = mc.get(key)
            work_log.debug(str(body))
            if body:
                recode = 0
                redata = body
            else:
                recode = 5

        elif task == "set":
            value = mc_task.get("mc_value")
            expire = int(mc_task.get("mc_expire"))
            body = mc.set(key, value, expire)
            work_log.debug(str(body))
            if body:
                recode = 0
            else:
                recode = 1
        elif task == "cleardata":
            recode = 2

        # data = {"recode": recode, "redata": body}
        # return data

        if recode == 0:
            return {"recode": 0, "redata": redata}
        elif recode == 1:
            return {"recode": 1, "redata": "run error"}
        elif recode == 2:
            return {"recode": 2, "redata": "暂不支持"}
        elif recode == 3:
            return {"recode": 3, "redata": "format error"}
        elif recode == 5:
            return {"recode": 5, "redata": "no data"}

        else:
            return {"recode": 4, "redata": "other error"}
