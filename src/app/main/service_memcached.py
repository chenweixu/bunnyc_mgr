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
    """docstring for Memcached_single"""

    def __init__(self, ip, port):
        super(Memcached_single, self).__init__()
        self.ip = ip
        self.port = port
        self.user = conf_data("user_info", "default_user")
        self.pidfile = conf_data("service_info", "memcached", "pidfile")
        self.start_cmd = conf_data("service_info", "memcached", "start_cmd")
        self.stop_cmd = conf_data("service_info", "memcached", "stop_cmd")

    def _mc_ssh_cmd(self, cmd):
        work_log.info("_mc_ssh_cmd host: %s cmd: %s" % (self.ip, cmd))
        try:
            ssh = HostBaseCmd(self.ip, user=self.user)
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
        return self._mc_ssh_cmd(cmd)

    def stop(self):
        mc_pidfile = self.pidfile.replace("1111", str(self.port))
        cmd = self.stop_cmd.replace("mc_pidfile", mc_pidfile)
        work_log.debug("stop_mc: %s" % cmd)
        return self._mc_ssh_cmd(cmd)

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
            server = MemcachedDataManager(host, port)
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
        self.stop_mc_group()
        time.sleep(2)
        data = self.start_mc_group()
        return data


class MemcachedManagerSingle(object):
    """docstring for MemcachedManagerSingle"""

    def __init__(self, ip, port):
        super(MemcachedManagerSingle, self).__init__()
        self.user = conf_data("user_info", "default_user")
        self.pidfile = conf_data("service_info", "memcached", "pidfile")
        self.start_cmd = conf_data("service_info", "memcached", "start_cmd")
        self.stop_cmd = conf_data("service_info", "memcached", "stop_cmd")
        self.ip = ip
        self.port = port

    def run_task(self, task):
        server = Memcached_single(self.ip, self.port)
        if task == "start":
            server.start()
        if task == "stop":
            server.stop()
        if task == "reboot":
            server.reboot()


class MemcachedManagerGroup(object):
    """docstring for MemcachedManagerGroup"""

    def __init__(self, group):
        super(MemcachedManagerGroup, self).__init__()
        self.group = group

    def run_task(self, task):
        if task == "start":
            pass
        if task == "stop":
            pass
        if task == "reboot":
            pass


class MemcachedDataManager(object):
    """docstring for MemcachedDataManager"""

    def __init__(self, ip, port):
        super(MemcachedDataManager, self).__init__()
        self.mc = Memcached(ip, port)

    def get(self, key):
        return {"recode": 0, "redata": self.mc.get(key)}

    def set(self, key, value, expire=600):
        return {"recode": 0, "redata": self.mc.set(key, value, expire)}

    def clear_data(self):
        return {"recode": 0, "redata": self.mc.flush_all()}

    def showstatus(self, key):
        return {"recode": 0, "redata": self.mc.show_stats(key)}

    def stats(self):
        return {"recode": 0, "redata": self.mc.stats()}

    # def get_connections_sum(self):
    #     return {"recode": 0, "redata": self.mc.get_connections_sum()}

    # def get_mc_base_info(self):
    #     curr_connections = self.mc.get_connections_sum()
    #     mem_user_rate = self.mc.get_mem_rate()
    #     if curr_connections != 0:
    #         check_ok = 0
    #     else:
    #         check_ok = 1
    #     return { "recode": check_ok, "redata": (curr_connections, mem_user_rate)}
