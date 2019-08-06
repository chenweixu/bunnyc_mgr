import time
from app.utils.memcached import Memcached
from app.main.conf import conf_data
from app.main.hostshell import HostBaseCmd
from app.main.hostshell import HostGroupCmd
from app import work_log


class Memcached_single(object):
    """docstring for Memcached_single"""

    def __init__(self, ip, port):
        super(Memcached_single, self).__init__()
        self.ip = ip
        self.port = port
        self.user = conf_data("user_info", "default_user")
        self.service_script = conf_data("service_info", "local_service_script")

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
            return str(e)

    def start(self):
        cmd = " ".join([self.service_script, "memcached", "start", str(self.port)])
        work_log.debug("start_mc: %s" % cmd)
        return self._mc_ssh_cmd(cmd)

    def stop(self):
        cmd = " ".join([self.service_script, "memcached", "stop", str(self.port)])
        work_log.debug("stop_mc: %s" % cmd)
        return self._mc_ssh_cmd(cmd)

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
            server = MemcachedDataSingle(host, port)
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


class MemcachedDataSingle(object):
    """docstring for MemcachedDataSingle"""

    def __init__(self, ip, port):
        super(MemcachedDataSingle, self).__init__()
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
        try:
            data = self.mc.stats_str()
            work_log.info(data)
            return {"recode": 0, "redata": data}
        except Exception as e:
            work_log.error("get memcached data error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "error"}

    def run_task(self, task):
        if task == "stats":
            return {"recode": 0, "redata": self.mc.stats()}
        if task == "info":
            return {"recode": 0, "redata": self.mc.stats()}


class MemcachedManagerSingle(object):
    """docstring for MemcachedManagerSingle"""

    def __init__(self, ip, port):
        super(MemcachedManagerSingle, self).__init__()
        self.ip = ip
        self.port = port

    def run_task(self, task):
        server = Memcached_single(self.ip, self.port)
        if task == "start":
            recode = server.start()
            if recode == 0:
                return {"recode": recode, "redata": "success"}
            else:
                return {"recode": 9, "redata": "exec error"}
        elif task == "stop":
            recode = server.stop()
            if recode == 0:
                return {"recode": recode, "redata": "success"}
            else:
                return {"recode": 9, "redata": "exec error"}
        elif task == "stats":
            info = MemcachedDataSingle(self.ip, self.port)
            return info.stats()
        elif task == "info":
            info = MemcachedDataSingle(self.ip, self.port)
            return info.stats()


# class MemcachedManagerGroup(object):
#     """docstring for MemcachedManagerGroup"""

#     def __init__(self, group):
#         super(MemcachedManagerGroup, self).__init__()
#         self.group = group

#     def run_task(self, task):
#         if task == "start":
#             pass
#         if task == "stop":
#             pass
#         if task == "reboot":
#             pass


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

