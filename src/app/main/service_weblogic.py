import itertools
from multiprocessing import Pool
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

    # def __init__(self):
    #     super(WeblogicManager, self).__init__()
    #     self.user = "weblogic"
    #     self.start_cmd = conf_data("service_info", "weblogic", "start_cmd")
    #     self.stop_cmd = conf_data("service_info", "weblogic", "stop_cmd")

    # def _weblogic_ssh_cmd(self, host, cmd, stdout=False):
    #     work_log.info("weblogic_ssh host: %s cmd: %s stdout: %s" % (host, cmd, stdout))
    #     try:
    #         ssh = HostBaseCmd(host, user=self.user)
    #         redata = ssh.ssh_cmd(cmd, stdout=stdout)

    #         if stdout:
    #             work_log.debug(str(stdout))
    #             return [redata[0], redata[1]]
    #         else:
    #             return redata
    #     except Exception as e:
    #         work_log.error("_weblogic_ssh_cmd Exception error")
    #         work_log.error(str(e))
    #         return 2

    # def list_service_group(self):
    #     data = conf_data("app_group")
    #     new_data = {}
    #     for i in data:
    #         new_data[i] = list(data.get(i).keys())
    #     return new_data

    # def get_check_task_url(self, groupname=None):
    #     interface = conf_data("service_info", "weblogic", "weblogic_interface")
    #     if groupname:
    #         group = conf_data("app_group", groupname)
    #         UrlList = []
    #         for host in group:
    #             for port in group.get(host):
    #                 url = "http://" + str(host) + ":" + str(port) + interface
    #                 UrlList.append(url)
    #         return UrlList
    #     else:
    #         group_all = conf_data("app_group")
    #         UrlList = []
    #         for group in group_all:
    #             for host in group_all.get(group):
    #                 for port in group_all.get(group).get(host):
    #                     url = "http://" + str(host) + ":" + str(port) + interface
    #                     UrlList.append(url)
    #         return UrlList

    # def check_weblogic_url(self, url):
    #     try:
    #         x = CheckWebInterface()
    #         recode = x.get_url_status_code(url, timeout=2)
    #         return [url, recode]
    #     except Exception as e:
    #         work_log.error("check_url----------")
    #         work_log.error(url)
    #         work_log.error(str(e))
    #         return [url, 1]

    # def check_weblogic(self, task, processes=6):
    #     pool = Pool(processes)
    #     result = []
    #     for url in task:
    #         result.append(pool.apply_async(self.check_weblogic_url, (url,)))
    #     pool.close()
    #     pool.join()

    #     data = {}
    #     for res in result:
    #         vle = res.get()
    #         if vle != 0:
    #             data[vle[0]] = vle[1]
    #     return data

    # def check_weblogic_group_interface(self, groupname=None):
    #     if groupname:
    #         UrlList = self.get_check_task_url(groupname)
    #         data = self.check_weblogic(UrlList, processes=10)
    #         return data
    #     else:
    #         UrlList = self.get_check_task_url()
    #         data = self.check_weblogic(UrlList, processes=80)
    #         return data

    # def start_weblogic_single_host(self, host):
    #     # 顺序 启动单个主机的6个服务
    #     data = []
    #     for serid in range(1, 7):
    #         port = 17100 + serid
    #         cmd = self.start_cmd.replace("1", str(serid))
    #         run_code = self._weblogic_ssh_cmd(host, cmd)
    #         data.append([host, port, run_code])
    #     return data

    # def start_weblogic_single_service(self, host, serid, status=None):
    #     # 启动单个服务
    #     port = 17100 + int(serid)
    #     cmd = self.start_cmd.replace("1", str(serid))
    #     run_code = self._weblogic_ssh_cmd(host, cmd)
    #     if status:
    #         return run_code
    #     else:
    #         return [host, port, run_code]

    # def start_wg_single(self, ip, app=None):
    #     # 并行 启动单个主机上的6个服务 | 或单个单个服务
    #     if app:
    #         data = self.start_weblogic_single_service(ip, app)
    #         return [data]
    #     else:
    #         pool = Pool(processes=6)
    #         info = []
    #         for serid in range(1, 7):
    #             info.append(
    #                 pool.apply_async(self.start_weblogic_single_service, (ip, serid))
    #             )
    #         pool.close()
    #         pool.join()

    #         data = []
    #         for i in info:
    #             data.append(i.get())
    #         return data

    # def start_wg_group(self, host_list):
    #     # 并行 启动多个主机上的6服务
    #     info = []
    #     pool = Pool(processes=16)

    #     for ip, serid in itertools.product(host_list, range(1, 7)):
    #         info.append(
    #             pool.apply_async(self.start_weblogic_single_service, (ip, serid))
    #         )
    #     pool.close()
    #     pool.join()

    #     data = []
    #     for i in info:
    #         data.append(i.get())
    #     return data

    # def stop_weblogic_single_hosts(self, host):
    #     # 顺序 停止单个主机上的6个服务
    #     data = []
    #     for serid in range(1, 7):
    #         port = 17100 + serid
    #         cmd = self.stop_cmd.replace("1", str(serid))

    #         run_code = self._weblogic_ssh_cmd(host, cmd)
    #         data.append([host, port, run_code])
    #     return data

    # def stop_weblogic_single_service(self, host, serid, status=None):
    #     # 停止 单个服务
    #     port = 17100 + serid
    #     cmd = self.stop_cmd.replace("1", str(serid))
    #     run_code = self._weblogic_ssh_cmd(host, cmd)

    #     if status:
    #         return run_code
    #     else:
    #         return [host, port, run_code]

    # def stop_wg_single(self, ip, app=None):
    #     # 并行 停止单个主机上的6个服务 | 或单个单个服务
    #     if app:
    #         data = self.stop_weblogic_single_service(ip, app)
    #         return [data]
    #     else:
    #         pool = Pool(processes=6)
    #         info = []
    #         for serid in range(1, 7):
    #             info.append(
    #                 pool.apply_async(self.stop_weblogic_single_service, (ip, serid))
    #             )
    #         pool.close()
    #         pool.join()

    #         data = []
    #         for i in info:
    #             data.append(i.get())
    #         return data

    # def stop_wg_group(self, host_list):
    #     # 并行 停止多个主机上的服务
    #     info = []
    #     pool = Pool(processes=16)

    #     for ip, serid in itertools.product(host_list, range(1, 7)):
    #         info.append(
    #             pool.apply_async(self.stop_weblogic_single_service, (ip, serid))
    #         )
    #     pool.close()
    #     pool.join()

    #     data = []
    #     for i in info:
    #         data.append(i.get())
    #     return data

    # def showlogaccess(self, host, app):
    #     log_access = conf_data("service_info", "weblogic", "log_access")
    #     cmd = "tail -n 300 " + log_access.replace("1", str(app))
    #     data = self._weblogic_ssh_cmd(host, cmd, stdout=True)
    #     if data == 2:
    #         return {"recode": data, "redata": "error"}
    #     else:
    #         return {"recode": data[0], "redata": data[1]}

    # def showlogout(self, host, app):
    #     log_out = conf_data("service_info", "weblogic", "log_out")
    #     cmd = "tail -n 300 " + log_out.replace("1", str(app))
    #     data = self._weblogic_ssh_cmd(host, cmd, stdout=True)
    #     if data == 2:
    #         return {"recode": data, "redata": "error"}
    #     else:
    #         return {"recode": data[0], "redata": data[1]}

    # def get_group_host(self, group):
    #     info = conf_data("app_group", group)
    #     new_data = []
    #     work_log.debug(str(new_data))
    #     for i in info:
    #         new_data.append(i)
    #     return new_data

    # def group_task_to_data(self, data):
    #     tmp1 = 0
    #     error_service = ""
    #     for i in data:
    #         if i[-1] == 0:
    #             tmp1 += 1
    #         else:
    #             error_service += str(i[1]) + " "

    #     if tmp1 == len(data):
    #         return {"recode": 0, "redata": "all success"}
    #     else:
    #         return {
    #             "recode": 5,
    #             "redata": "not all success, error service: " + error_service.rstrip(),
    #         }

    # def run_task(self, task, host, port=None):
    #     if not port:
    #         work_log.info("weblogic task: %s, obj host all service" % task)

    #         if task == "start":
    #             work_log.debug("weblogic task start all")
    #             body = self.start_wg_single(host)
    #             tmp1 = 0
    #             error_service = ""
    #             for i in body:
    #                 if i[-1] == 0:
    #                     tmp1 += 1
    #                 else:
    #                     error_service += str(i[1]) + " "

    #             if tmp1 == 6:
    #                 return {"recode": 0, "redata": "all success"}
    #             else:
    #                 return {
    #                     "recode": 2,
    #                     "redata": "not all success, error service: "
    #                     + error_service.rstrip(),
    #                 }

    #         elif task == "stop":
    #             work_log.debug("weblogic task: stop all")
    #             body = self.stop_wg_single(host)
    #             tmp1 = 0
    #             error_service = ""
    #             for i in body:
    #                 if i[-1] == 0:
    #                     tmp1 += 1
    #                 else:
    #                     error_service += str(i[1]) + " "

    #             if tmp1 == 6:
    #                 return {"recode": 0, "redata": "all success"}
    #             else:
    #                 return {
    #                     "recode": 1,
    #                     "redata": "not all success, error service: "
    #                     + error_service.rstrip(),
    #                 }
    #     elif port >= 1 and port <= 6:
    #         work_log.info("weblogic task: %s, obj service port: %s" % (task, port))
    #         if task == "start":
    #             work_log.debug("weblogic task: " + str(task) + "port: " + str(port))
    #             data = self.start_weblogic_single_service(host, port, status=True)

    #             if data == 0:
    #                 redata = "success"
    #             else:
    #                 redata = "error"
    #             return {"recode": data, "redata": redata}

    #         elif task == "stop":
    #             work_log.debug("weblogic task: " + str(task) + "port: " + str(port))
    #             data = self.stop_weblogic_single_service(host, port, status=True)
    #             if data == 0:
    #                 redata = "success"
    #             else:
    #                 redata = "error"
    #             return {"recode": data, "redata": redata}

    #         elif task == "accesslog":
    #             work_log.debug("weblogic task: " + str(task))
    #             return self.showlogaccess(host, port)
    #         elif task == "projectlog":
    #             work_log.debug("weblogic task: " + str(task))
    #             return self.showlogout(host, port)

    #     else:
    #         return {"recode": 1, "redata": "参数错误"}

    # def run_task_group(self, task, group):
    #     work_log.debug("weblogic task: " + str(task))
    #     work_log.debug("weblogic group: " + str(group))
    #     host_list = self.get_group_host(group)
    #     if task == "start":
    #         data = self.start_wg_group(host_list)
    #         new_data = self.group_task_to_data(data)
    #     elif task == "stop":
    #         data = self.stop_wg_group(host_list)
    #         new_data = self.group_task_to_data(data)
    #     elif task == "check":
    #         pass
    #     return new_data


class WeblogicManagerSingle(object):
    """docstring for WeblogicManagerSingle"""
    def __init__(self, ip, port=None):
        super(WeblogicManagerSingle, self).__init__()
        self.ip = ip
        self.port = port
        self.user = conf_data("service_info", "weblogic", "default_user")
        self.start_cmd = conf_data("service_info", "weblogic", "start_cmd")
        self.stop_cmd = conf_data("service_info", "weblogic", "stop_cmd")

    def _weblogic_ssh_cmd(self, cmd):
        work_log.info("weblogic_ssh host: %s cmd: %s" % (self.ip, cmd))
        try:
            ssh = HostBaseCmd(self.ip, user=self.user)
            data = ssh.ssh_cmd(cmd, stdout=True)
            work_log.debug("_weblogic_ssh_cmd redata: %s" % str(data))
            return data
        except Exception as e:
            work_log.error("_weblogic_ssh_cmd Exception error")
            work_log.error(str(e))
            return 2

    def start_weblogic_single_service(self, port=None):
        # 启动单个服务
        if not port:
            cmd = self.start_cmd.replace("1", str(int(self.port) - 17100))
        else:
            cmd = self.start_cmd.replace("1", str(int(port) - 17100))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": "success"}
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}


    def stop_weblogic_single_service(self, port=None):
        # 停止单个服务
        if not port:
            cmd = self.stop_cmd.replace("1", str(int(self.port) - 17100))
        else:
            cmd = self.stop_cmd.replace("1", str(int(port) - 17100))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": "success"}
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}

    def reboot_weblogic_single_service(self):
        data = self.stop_weblogic_single_service()
        if data.get("recode") != 0:
            return data
        else:
            return self.start_weblogic_single_service()

    def showlogaccess(self):
        log_access = conf_data("service_info", "weblogic", "log_access")
        cmd = "tail -n 300 " + log_access.replace("1", str(int(self.port) - 17100))
        data = self._weblogic_ssh_cmd(cmd)
        if data == 2:
            return {"recode": data, "redata": "error"}
        else:
            return {"recode": data[0], "redata": data[1]}

    def showprojectlog(self):
        log_out = conf_data("service_info", "weblogic", "log_out")
        cmd = "tail -n 300 " + log_out.replace("1", str(int(self.port) - 17100))
        data = self._weblogic_ssh_cmd(cmd)
        if data == 2:
            return {"recode": data, "redata": "error"}
        else:
            return {"recode": data[0], "redata": data[1]}

    def start_wg_single(self):
        # 并行 启动单个主机上的6个服务
        pool = Pool(processes=6)
        info = []
        for port in range(17101, 17107):
            info.append(
                pool.apply_async(self.start_weblogic_single_service, (port,))
            )
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        work_log.info(str(data))
        return data

    def stop_wg_single(self):
        # 并行 停止单个主机上的6个服务
        pool = Pool(processes=6)
        info = []
        for port in range(17101, 17107):
            info.append(
                pool.apply_async(self.stop_weblogic_single_service, (port,))
            )
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        work_log.info(str(data))
        return data


    def start_weblogic_single_host(self, host):
        # 顺序 启动单个主机的6个服务
        data = []
        for serid in range(1, 7):
            port = 17100 + serid
            cmd = self.start_cmd.replace("1", str(serid))
            run_code = self._weblogic_ssh_cmd(cmd)
            data.append([host, port, run_code])
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



    def run_task(self, task):
        work_log.info('weblogic service task: %s , host: %s port: %s' % (task, self.ip, self.port))
        if self.port and self.port >= 17101 and self.port <= 17106:
            try:
                if task == "start":
                    return self.start_weblogic_single_service()
                elif task == "stop":
                    return self.stop_weblogic_single_service()
                elif task == "reboot":
                    return self.reboot_weblogic_single_service
                elif task == "accesslog":
                    return self.showlogaccess()
                elif task == "projectlog":
                    return self.showprojectlog()
                elif task == "check":
                    pass
            except Exception as e:
                work_log.error("single weblogic service run error")
                work_log.error(str(e))
                return {"recode": 2, "redata": str(e)}

        elif not self.port:
            work_log.info('not port')
            try:
                if task == "start":
                    return self.start_wg_single()
                elif task == "stop":
                    return self.stop_wg_single()
                elif task == "reboot":
                    return self.reboot_weblogic_single_service
                elif task == "accesslog":
                    return self.showlogaccess()
                elif task == "projectlog":
                    return self.showprojectlog()
                elif task == "check":
                    pass
            except Exception as e:
                work_log.error("single weblogic service run error")
                work_log.error(str(e))
                return {"recode": 2, "redata": str(e)}


        #         body = self.start_wg_single(host)
        #         tmp1 = 0
        #         error_service = ""
        #         for i in body:
        #             if i[-1] == 0:
        #                 tmp1 += 1
        #             else:
        #                 error_service += str(i[1]) + " "

        #         if tmp1 == 6:
        #             return {"recode": 0, "redata": "all success"}
        #         else:
        #             return {
        #                 "recode": 2,
        #                 "redata": "not all success, error service: "
        #                 + error_service.rstrip(),
        #             }

        #     elif task == "stop":
        #         work_log.debug("weblogic task: stop all")
        #         body = self.stop_wg_single(host)
        #         tmp1 = 0
        #         error_service = ""
        #         for i in body:
        #             if i[-1] == 0:
        #                 tmp1 += 1
        #             else:
        #                 error_service += str(i[1]) + " "

        #         if tmp1 == 6:
        #             return {"recode": 0, "redata": "all success"}
        #         else:
        #             return {
        #                 "recode": 1,
        #                 "redata": "not all success, error service: "
        #                 + error_service.rstrip(),
        #             }
        # elif port >= 1 and port <= 6:
        #     work_log.info("weblogic task: %s, obj service port: %s" % (task, port))
        #     if task == "start":
        #         work_log.debug("weblogic task: " + str(task) + "port: " + str(port))
        #         data = self.start_weblogic_single_service(host, port, status=True)

        #         if data == 0:
        #             redata = "success"
        #         else:
        #             redata = "error"
        #         return {"recode": data, "redata": redata}

        #     elif task == "stop":
        #         work_log.debug("weblogic task: " + str(task) + "port: " + str(port))
        #         data = self.stop_weblogic_single_service(host, port, status=True)
        #         if data == 0:
        #             redata = "success"
        #         else:
        #             redata = "error"
        #         return {"recode": data, "redata": redata}

        #     elif task == "accesslog":
        #         work_log.debug("weblogic task: " + str(task))
        #         return self.showlogaccess(host, port)
        #     elif task == "projectlog":
        #         work_log.debug("weblogic task: " + str(task))
        #         return self.showlogout(host, port)

        else:
            return {"recode": 1, "redata": "参数错误"}

class WeblogicManagerGroup(object):
    """docstring for WeblogicManagerGroup"""
    def __init__(self):
        super(WeblogicManagerGroup, self).__init__()


    def list_service_group(self):
        data = conf_data("app_group")
        new_data = {}
        for i in data:
            new_data[i] = list(data.get(i).keys())
        return new_data

    def start_weblogic_single_service(ip, serid):
        server = WeblogicManagerSingle(ip, serid)
        server.start_weblogic_single_service()

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
        if task == "start":
            data = self.start_wg_group(host_list)
            new_data = self.group_task_to_data(data)
        elif task == "stop":
            data = self.stop_wg_group(host_list)
            new_data = self.group_task_to_data(data)
        elif task == "check":
            pass
        return new_data

class WeblogicManagerCheck(object):
    """docstring for WeblogicManagerCheck"""
    def __init__(self):
        super(WeblogicManagerCheck, self).__init__()

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

