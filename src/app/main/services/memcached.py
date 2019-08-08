import time
from app.utils.memcached import Memcached
from app.main.conf import conf_data
from app.main.server.hostbase import HostBaseCmd
from app.main.server.hostgroup import HostGroupCmd
from app import work_log
from multiprocessing import Pool

class MemcachedManagerSingle(object):
    """docstring for MemcachedManagerSingle"""

    def __init__(self, ip, port):
        super(MemcachedManagerSingle, self).__init__()
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

    def run_task(self, task):
        if task == "start":
            recode = self.start()
            if recode == 0:
                return {"recode": recode, "redata": "success"}
            else:
                return {"recode": 9, "redata": "exec error"}
        elif task == "stop":
            recode = self.stop()
            if recode == 0:
                return {"recode": recode, "redata": "success"}
            else:
                return {"recode": 9, "redata": "exec error"}



class MemcachedManagerGroup(object):
    """docstring for MemcachedManagerGroup"""

    def __init__(self, group=None, mc_list=None):
        super(MemcachedManagerGroup, self).__init__()
        self.group = group
        self.mc_list = mc_list

    def get_group_data(self):
        unit_list = []
        if self.group:
            info = conf_data("mc_group", self.group)
            for i in info:
                ip = i.split()[0]
                port = i.split()[1]
                unit_list.append([ip, port])
            return unit_list
        if self.mc_list:
            for i in self.mc_list:
                host = i.split()[0]
                port = i.split()[1]
                unit_list.append([ip, port])
            return unit_list

    def single_task(self, server, task):
        s1 = MemcachedManagerSingle(server[0], server[1])
        data = s1.run_task(task)
        data["ip"] = server[0]
        # if data.get("recode") != 0:
        #     data["redata"] = "error"
        # else:
        #     data["redata"] = "success"
        return data

    def group_task(self, task):
        info = []
        pool = Pool(processes=10)
        for server in self.get_group_data():
            info.append(pool.apply_async(self.single_task, (server, task)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def run_task(self, task):
        if task == "start" or task == "stop":
            return self.group_task(task)


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



        # elif task == "stats":
        #     info = MemcachedDataSingle(self.ip, self.port)
        #     return info.stats()
        # elif task == "info":
        #     info = MemcachedDataSingle(self.ip, self.port)
        #     return info.stats()



class MemcachedDataGroup(object):
    """docstring for MemcachedDataGroup"""
    def __init__(self, group=None, mc_list=None):
        super(MemcachedDataGroup, self).__init__()
        self.group = group
        self.mc_list = mc_list

    def get_group_data(self):
        unit_list = []
        if self.group:
            info = conf_data("mc_group", self.group)
            for i in info:
                ip = i.split()[0]
                port = i.split()[1]
                unit_list.append([ip, port])
            return unit_list
        if self.mc_list:
            for i in self.mc_list:
                host = i.split()[0]
                port = i.split()[1]
                unit_list.append([ip, port])
            return unit_list

    def single_task(self, server, task):
        s1 = MemcachedDataSingle(server[0], server[1])
        # if task == 'get':

        data = s1.run_task(task)
        # data["ip"] = server[0]
        return data

    def group_task(self, task):
        info = []
        pool = Pool(processes=10)
        for server in self.get_group_data():
            info.append(pool.apply_async(self.single_task, (server, task)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def run_task(self, task):
        if task == "start" or task == "stop":
            return self.group_task(task)

    def get(self, key):
        pass

    def set(self, key):
        pass

    def delete(self, key):
        pass

    def clear(self):
        data = []
        for i in self.get_group_data():
            host = i.split()[0]
            port = i.split()[1]
            server = MemcachedDataSingle(host, port)
            status = server.clear_data()
            data.append((host, port, status))
        return data

    def stats(self):
        pass

    def info(self):
        pass
