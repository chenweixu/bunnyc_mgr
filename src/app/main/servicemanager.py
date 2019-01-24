import socket
import time
import requests
import itertools
import re
from multiprocessing import Pool
from app.main.util.memcached import Memcached
from app.main.conf import conf_data
from app.main.util.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.hostshell import HostGroupCmd
from app.main.web import CheckWebInterface

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class WeblogicManager(object):
    """docstring for WeblogicManager"""

    def __init__(self):
        super(WeblogicManager, self).__init__()
        self.user = "weblogic"
        self.start_cmd = conf_data("service_info", "weblogic", "start_cmd")
        self.stop_cmd = conf_data("service_info", "weblogic", "stop_cmd")

    def _weblogic_ssh_cmd(self, host, cmd, stdout=False):
        work_log.info("weblogic_ssh host: %s cmd: %s stdout: %s" % (host, cmd, stdout))
        try:
            ssh = HostBaseCmd(host, user=self.user)
            redata = ssh.ssh_cmd(cmd, stdout=stdout)

            if stdout:
                work_log.debug(str(stdout))
                return [redata[0], redata[1]]
            else:
                return redata
        except Exception as e:
            work_log.error("_weblogic_ssh_cmd Exception error")
            work_log.error(str(e))
            return 2

    def list_service_group(self):
        data = conf_data("app_group")
        new_data = {}
        for i in data:
            new_data[i] = list(data.get(i).keys())
        return new_data

    def get_check_task_url(self, groupname=None):
        interface = conf_data("service_info", "weblogic", "weblogic_interface")
        if groupname:
            group = conf_data("app_group", groupname)
            UrlList = []
            for host in group:
                for port in group.get(host):
                    url = "http://" + str(host) + ":" + str(port) + interface
                    UrlList.append(url)
            return UrlList
        else:
            group_all = conf_data("app_group")
            UrlList = []
            for group in group_all:
                for host in group_all.get(group):
                    for port in group_all.get(group).get(host):
                        url = "http://" + str(host) + ":" + str(port) + interface
                        UrlList.append(url)
            return UrlList

    def check_weblogic_url(self, url):
        try:
            x = CheckWebInterface()
            recode = x.get_url_status_code(url, timeout=2)
            return [url, recode]
        except Exception as e:
            work_log.error("check_url----------")
            work_log.error(url)
            work_log.error(str(e))
            return [url, 1]

    def check_weblogic(self, task, processes=6):
        pool = Pool(processes)
        result = []
        for url in task:
            result.append(pool.apply_async(self.check_weblogic_url, (url,)))
        pool.close()
        pool.join()

        data = {}
        for res in result:
            vle = res.get()
            if vle != 0:
                data[vle[0]] = vle[1]
        return data

    def check_weblogic_group_interface(self, groupname=None):
        if groupname:
            UrlList = self.get_check_task_url(groupname)
            data = self.check_weblogic(UrlList, processes=10)
            return data
        else:
            UrlList = self.get_check_task_url()
            data = self.check_weblogic(UrlList, processes=80)
            return data

    def start_weblogic_single_host(self, host):
        # 顺序 启动单个主机的6个服务
        data = []
        for serid in range(1, 7):
            port = 17100 + serid
            cmd = self.start_cmd.replace("1", str(serid))
            run_code = self._weblogic_ssh_cmd(host, cmd)
            data.append([host, port, run_code])
        return data

    def start_weblogic_single_service(self, host, serid, status=None):
        # 启动单个服务
        port = 17100 + int(serid)
        cmd = self.start_cmd.replace("1", str(serid))
        run_code = self._weblogic_ssh_cmd(host, cmd)
        if status:
            return run_code
        else:
            return [host, port, run_code]

    def start_wg_single(self, ip, app=None):
        # 并行 启动单个主机上的6个服务 | 或单个单个服务
        if app:
            data = self.start_weblogic_single_service(ip, app)
            return [data]
        else:
            pool = Pool(processes=6)
            info = []
            for serid in range(1, 7):
                info.append(
                    pool.apply_async(self.start_weblogic_single_service, (ip, serid))
                )
            pool.close()
            pool.join()

            data = []
            for i in info:
                data.append(i.get())
            return data

    def start_wg_group(self, host_list):
        # 并行 启动多个主机上的6服务
        info = []
        pool = Pool(processes=16)

        for ip, serid in itertools.product(host_list, range(1, 7)):
            info.append(
                pool.apply_async(self.start_weblogic_single_service, (ip, serid))
            )
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def stop_weblogic_single_hosts(self, host):
        # 顺序 停止单个主机上的6个服务
        data = []
        for serid in range(1, 7):
            port = 17100 + serid
            cmd = self.stop_cmd.replace("1", str(serid))

            run_code = self._weblogic_ssh_cmd(host, cmd)
            data.append([host, port, run_code])
        return data

    def stop_weblogic_single_service(self, host, serid, status=None):
        # 停止 单个服务
        port = 17100 + serid
        cmd = self.stop_cmd.replace("1", str(serid))
        run_code = self._weblogic_ssh_cmd(host, cmd)

        if status:
            return run_code
        else:
            return [host, port, run_code]

    def stop_wg_single(self, ip, app=None):
        # 并行 停止单个主机上的6个服务 | 或单个单个服务
        if app:
            data = self.stop_weblogic_single_service(ip, app)
            return [data]
        else:
            pool = Pool(processes=6)
            info = []
            for serid in range(1, 7):
                info.append(
                    pool.apply_async(self.stop_weblogic_single_service, (ip, serid))
                )
            pool.close()
            pool.join()

            data = []
            for i in info:
                data.append(i.get())
            return data

    def stop_wg_group(self, host_list):
        # 并行 停止多个主机上的服务
        info = []
        pool = Pool(processes=16)

        for ip, serid in itertools.product(host_list, range(1, 7)):
            info.append(
                pool.apply_async(self.stop_weblogic_single_service, (ip, serid))
            )
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def showlogaccess(self, host, app):
        log_access = conf_data("service_info", "weblogic", "log_access")
        cmd = 'tail -n 300 ' + log_access.replace("1", str(app))
        data = self._weblogic_ssh_cmd(host, cmd, stdout=True)
        if data == 2:
            return {"recode": data, "redata": "error"}
        else:
            return {"recode": data[0], "redata": data[1]}

    def showlogout(self, host, app):
        log_out = conf_data("service_info", "weblogic", "log_out")
        cmd = 'tail -n 300 ' + log_out.replace("1", str(app))
        data = self._weblogic_ssh_cmd(host, cmd, stdout=True)
        if data == 2:
            return {"recode": data, "redata": "error"}
        else:
            return {"recode": data[0], "redata": data[1]}

    def run_task(self, host, task, app_id=None):
        if app_id != "all":
            app_id = int(app_id)

        if task == "start" and app_id == "all":
            work_log.debug("weblogic task: " + str(task))
            body = self.start_wg_single(host)
            tmp1 = 0
            error_service = ""
            for i in body:
                if i[-1] == 0:
                    tmp1 += 1
                else:
                    error_service += str(i[1]) + " "

            if tmp1 == 6:
                return {"recode": 0, "redata": "all success"}
            else:
                return {
                    "recode": 5,
                    "redata": "not all success, error service: "
                    + error_service.rstrip(),
                }

        elif task == "stop" and app_id == "all":
            work_log.debug("weblogic task: " + str(task))
            body = self.stop_wg_single(host)
            tmp1 = 0
            error_service = ""
            for i in body:
                if i[-1] == 0:
                    tmp1 += 1
                else:
                    error_service += str(i[1]) + " "

            if tmp1 == 6:
                return {"recode": 0, "redata": "all success"}
            else:
                return {
                    "recode": 5,
                    "redata": "not all success, error service: "
                    + error_service.rstrip(),
                }

        elif task == "start" and app_id >= 1 and app_id <= 6:
            work_log.debug("weblogic task: " + str(task) + "app_id: " + str(app_id))
            data = self.start_weblogic_single_service(host, app_id, status=True)

            if data == 0:
                redata = "success"
            else:
                redata = "error"
            return {"recode": data, "redata": redata}

        elif task == "stop" and app_id >= 1 and app_id <= 6:
            work_log.debug("weblogic task: " + str(task) + "app_id: " + str(app_id))
            data = self.stop_weblogic_single_service(host, app_id, status=True)
            if data == 0:
                redata = "success"
            else:
                redata = "error"
            return {"recode": data, "redata": redata}

        elif task == "show_access_log" and app_id != "all":
            work_log.debug("weblogic task: " + str(task))
            data = self.showlogaccess(host, app_id)
        elif task == "show_error_log" and app_id != "all":
            work_log.debug("weblogic task: " + str(task))
            data = self.showlogout(host, app_id)
        else:
            data = {"recode": 2, "redata": "参数错误"}

        return data

    def get_group_host(self, group):
        info = conf_data("app_group", group)
        new_data = []
        work_log.debug(str(new_data))
        for i in info:
            new_data.append(i)
        return new_data

    def group_task_to_data(self, data):
        tmp1 = 0
        error_service = ""
        for i in data:
            if i[-1] == 0:
                tmp1 += 1
            else:
                error_service += str(i[1]) + " "

        if tmp1 == len(data):
            return {"recode": 0, "redata": "all success"}
        else:
            return {
                "recode": 5,
                "redata": "not all success, error service: " + error_service.rstrip(),
            }

    def run_task_group(self, task, group):
        work_log.debug("weblogic task: " + str(task))
        work_log.debug("weblogic group: " + str(group))
        host_list = self.get_group_host(group)
        if task == "start_group":
            data = self.start_wg_group(host_list)
            new_data = self.group_task_to_data(data)
        elif task == "stop_group":
            data = self.stop_wg_group(host_list)
            new_data = self.group_task_to_data(data)
        return new_data


class MemcachedManager(object):
    """docstring for MemcachedManager"""

    def __init__(self):
        super(MemcachedManager, self).__init__()
        self.user = conf_data('user_info','default_user')
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

    def _clear_mc(self, host, port):
        mc = Memcached(host, int(port))
        try:
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
            return 91

    def clear_mc_group(self, mc_list):
        data = []
        for i in mc_list:
            host = i.split()[0]
            port = i.split()[1]
            status = self._clear_mc(host, port)
            data.append((host, port, status))
        return data

    def start_mc(self, host, port):
        mc_pidfile = self.pidfile.replace("1111", str(port))
        cmd1 = self.start_cmd.replace("mc_port", str(port))
        cmd = cmd1.replace("mc_pidfile", mc_pidfile)
        work_log.debug("start_mc: %s" % cmd)
        return self._mc_ssh_cmd(host, cmd)

    def start_mc_group(self, mc_list):
        data = []
        for i in mc_list:
            host = i.split()[0]
            port = i.split()[1]
            status = self.start_mc(host, port)
            data.append((host, port, status))
        return data

    def stop_mc(self, host, port):
        mc_pidfile = self.pidfile.replace("1111", str(port))
        cmd = self.stop_cmd.replace("mc_pidfile", mc_pidfile)
        work_log.debug("stop_mc: %s" % cmd)
        return self._mc_ssh_cmd(host, cmd)

    def stop_mc_group(self, mc_list):
        data = []
        for i in mc_list:
            host = i.split()[0]
            port = i.split()[1]
            status = self.stop_mc(host, port)
            data.append((host, port, status))
        return data

    def reboot_mc_group(self, mc_list):
        work_log.debug("reboot mc group: " + str(mc_list))
        self.stop_mc_group(mc_list)
        time.sleep(2)
        data = self.start_mc_group(mc_list)
        return data

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

    def run_task(self, mc_task):
        work_log.debug("MemcachedManager run task")
        work_log.debug("mc_task: " + str(mc_task))
        task = mc_task.get("task")
        mc_obj = mc_task.get("mc_addr")

        if mc_obj == "all":
            recode = 2
        elif mc_obj in ["dmz", "cd"]:
            mc_list = conf_data("service_info", "memcached", mc_obj)
            if task == "start":
                recode = self.start_mc_group(mc_list)
            elif task == "stop":
                recode = self.stop_mc_group(mc_list)
            elif task == "reboot":
                recode = self.reboot_mc_group(mc_list)
            else:
                recode = 3
        else:
            mc_addr = mc_obj.split(":")[0]
            mc_port = int(mc_obj.split(":")[1])
            if task == "start":
                recode = self.start_mc(mc_addr, mc_port)
            elif task == "stop":
                recode = self.stop_mc(mc_addr, mc_port)
            elif task == "reboot":
                self.stop_mc(mc_addr, mc_port)
                time.sleep(1)
                recode = self.start_mc(mc_addr, mc_port)
            else:
                recode = 3

        if recode == 0:
            return {"recode": 0, "redata": "run succsse"}
        elif recode == 1:
            return {"recode": 1, "redata": "run error"}
        elif recode == 2:
            return {"recode": 2, "redata": "暂不支持"}
        elif recode == 3:
            return {"recode": 3, "redata": "format error"}
        else:
            return {"recode": 4, "redata": "other error"}

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


class NginxManager(object):
    """docstring for NginxManager"""

    def __init__(self):
        super(NginxManager, self).__init__()
        self.user = conf_data("user_info", "default_user")

    def __ssh_cmd(self, host, cmd):
        a = HostBaseCmd(host, self.user)
        status, data = a.ssh_cmd(cmd, stdout=True)
        return status, data

    def showlockip(self):
        cmd = "grep clientRealIp /opt/nginx/conf/deny_ip.conf"
        ip = conf_data("service_info", "nginx", "dmz")[0]
        recode, data = self.__ssh_cmd(ip, cmd)
        lock_ip = re.compile("\d+.\d+.\d+.\d+").findall(data)
        work_log.debug("showlockip: " + str(lock_ip))
        return {"recode": 0, "data": lock_ip}
        # return {'recode':500,'data':'req not support'}

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
        elif task == "showlock":
            return self.showlockip()
        else:
            return {"recode": 9999, "data": "req format error"}

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
            data = "exec sucess"

        newdata = {"redata": data, "recode": recode}
        return newdata
