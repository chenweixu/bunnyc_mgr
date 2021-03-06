import itertools
from multiprocessing import Pool
from app.main.conf import conf_data
from app.main.server.hostbase import HostBaseCmd
from app.main.server.hostgroup import HostGroupCmd
from app.main.services.web import CheckWebInterface
from app import work_log


class WeblogicManagerSingle(object):
    """docstring for WeblogicManagerSingle
    单机管理
    """

    def __init__(self, ip, port=None):
        super(WeblogicManagerSingle, self).__init__()
        self.ip = ip
        self.port = port
        self.user = conf_data("service_info", "weblogic", "default_user")
        self.service_script = conf_data("service_info", "local_service_script")

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
            return [2, str(e)]

    def start_weblogic_single_service(self, port=None):
        '''port 为给此函数传的参数，如过没有则使用类中的端口'''
        work_log.debug("start_weblogic_single_service")
        if not port:
            # all service
            cmd = " ".join(
                [self.service_script, "weblogic", "start", str(int(self.port) - 17100)]
            )
        else:
            cmd = " ".join(
                [self.service_script, "weblogic", "start", str(int(port) - 17100)]
            )
        work_log.debug(str(cmd))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def stop_weblogic_single_service(self, port=None):
        # 停止单个服务
        if not port:
            cmd = " ".join(
                [self.service_script, "weblogic", "stop", str(int(self.port) - 17100)]
            )
        else:
            cmd = " ".join(
                [self.service_script, "weblogic", "stop", str(int(port) - 17100)]
            )
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def showlogaccess(self):
        # 查看访问日志
        log_access = conf_data("service_info", "weblogic", "log_access")
        cmd = "tail -n 300 " + log_access.replace("1", str(int(self.port) - 17100))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def showprojectlog(self):
        # 查看业务日志
        log_out = conf_data("service_info", "weblogic", "log_out")
        cmd = "tail -n 500 " + log_out.replace("1", str(int(self.port) - 17100))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def showgclog(self):
        # 查看GC日志
        cmd = " ".join(
            [self.service_script, "weblogic", "gclog", str(int(self.port) - 17100)]
        )
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def start_wg_single(self):
        # 并行 启动单个主机上的6个服务
        cmd = " ".join([self.service_script, "weblogic", "start_group"])
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def stop_wg_single(self):
        # 并行 停止单个主机上的6个服务
        cmd = " ".join([self.service_script, "weblogic", "stop_group"])
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def single_service(self, task):
        # work_log.info("service weblogic task: %s , host: %s port: %s" % (task, self.ip, self.port))
        work_log.info(f"service weblogic task: {task} , host: {self.ip} port: {self.port}")

        try:
            if task == "start":
                return self.start_weblogic_single_service()
            elif task == "stop":
                return self.stop_weblogic_single_service()
            elif task == "accesslog":
                return self.showlogaccess()
            elif task == "projectlog":
                return self.showprojectlog()
            elif task == "gclog":
                return self.showgclog()
            elif task == "check":
                work_log.info('check task')
                info = WeblogicManagerCheck()
                data = info.get_wg_single_service_status(self.ip, self.port)
                return {"recode": 0, "redata": data}
        except Exception as e:
            work_log.error("single weblogic service run error")
            work_log.error(str(e))
            return {"recode": 2, "redata": str(e)}

    def single_host_server(self, task):
        work_log.info("server weblogic task not port, all service")
        try:
            if task == "start":
                return self.start_wg_single()
            elif task == "stop":
                return self.stop_wg_single()
            elif task == "check":
                info = WeblogicManagerCheck()
                data = info.get_wg_single_server_status(self.ip)
                return {"recode": 0, "redata": data}
            else:
                return {"recode": 4, "redata": "不支持该操作"}
        except Exception as e:
            work_log.error("single weblogic service run error")
            work_log.error(str(e))
            return {"recode": 2, "redata": str(e)}

    def run_task(self, task):
        if self.port and int(self.port) >= 17101 and int(self.port) <= 17106:
            return self.single_service(task)
        elif not self.port:
            work_log.debug('single no port')
            return self.single_host_server(task)
        else:
            return {"recode": 1, "redata": "参数错误"}


class WeblogicManagerGroup(object):
    """docstring for WeblogicManagerGroup
    主机组管理
    """

    def __init__(self, group):
        super(WeblogicManagerGroup, self).__init__()
        self.group = group

    def get_group_host(self):
        info = conf_data("app_group", self.group)
        return info.keys()

    def start_single_host(self, ip):
        server = WeblogicManagerSingle(ip)
        data = server.start_wg_single()
        data["ip"] = ip
        if data.get("recode") != 0:
            data["redata"] = "error"
        else:
            data["redata"] = "success"
        return data

    def stop_single_host(self, ip):
        server = WeblogicManagerSingle(ip)
        data = server.stop_wg_single()
        data["ip"] = ip
        if data.get("recode") != 0:
            data["redata"] = "error"
        else:
            data["redata"] = "success"
        return data

    def start_wg_group(self):
        info = []
        pool = Pool(processes=10)
        for ip in self.get_group_host():
            info.append(pool.apply_async(self.start_single_host, (ip,)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def stop_wg_group(self):
        info = []
        pool = Pool(processes=10)
        for ip in self.get_group_host():
            info.append(pool.apply_async(self.stop_single_host, (ip,)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def checkRunData(self, data):
        if data.get("recode") == 0:
            return 0
        else:
            return 1

    def run_task_group(self, task):
        work_log.debug(f"weblogic group: {self.group}, task: {task}")
        try:
            if task == "start":
                data = self.start_wg_group()
            elif task == "stop":
                data = self.stop_wg_group()
            else:
                return {"recode": 9, "redata": "参数错误"}

            if any(map(self.checkRunData, data)):
                return {"recode": 2, "redata": data}
            else:
                return {"recode": 0, "redata": data}

        except Exception as e:
            work_log.error("run_task_group task error")
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}


class WeblogicManagerCheck(object):
    """docstring for WeblogicManagerCheck"""

    def __init__(self):
        super(WeblogicManagerCheck, self).__init__()

    def get_wg_check_url(self,ip, port):
        '''拼接任务URL'''
        return f"http://{ip}:{port}" + conf_data(
                        "service_info", "weblogic", "weblogic_interface"
                    )

    def check_url_status(self, url):
        '''检查一个URL-返回状态码'''
        try:
            x = CheckWebInterface()
            recode = x.get_url_status_code(url, timeout=2)
            return recode
        except Exception as e:
            work_log.error(f"check wg url error: {url}")
            work_log.error(str(e))
            return 999

    def check_weblogic_url(self, url):
        '''检查一个URL-返回数组'''
        try:
            x = CheckWebInterface()
            recode = x.get_url_status_code(url, timeout=2)
            return [url, recode]
        except Exception as e:
            work_log.error(f"check wg url error: {url}")
            work_log.error(str(e))
            return [url, 1]

    def get_host_task(self, ip):
        '''获取一个主机的任务列表'''
        data = []
        for i in conf_data("app_group").values():
            if ip in i:
                for port in i.get(ip):
                    data.append([ip, port])
        return data
        work_log.info(data)

    def check_weblogic(self, task, processes=6):
        '''并行执行任务'''
        pool = Pool(processes)
        result = []
        for url in task:
            result.append(pool.apply_async(self.check_weblogic_url, (url,)))
        pool.close()
        pool.join()

        data = []
        for res in result:
            vle = res.get()
            if vle != 0:
                data.append(vle)
        return data

    def get_wg_single_service_status(self, ip, port):
        '''检查一个服务的服务'''
        self.get_host_task(ip)
        url = self.get_wg_check_url(ip, port)
        return [url, self.check_url_status(url)]

    def get_wg_single_server_status(self, ip):
        '''获取一个主机服务的状态'''
        task_list = self.get_host_task(ip)
        data = []
        # num = 1
        for x,port in task_list:
            url = self.get_wg_check_url(ip, port)
            status = self.check_url_status(url)
            data.append([url, status])
            # data.append({'id': num,'url': url,'status': status})
            # num += 1
        return data

    def check_group_weblogic_interface(self, groupname):
        '''检查一组服务'''

        UrlList = []
        for x, y in conf_data("app_group", groupname).items():
            for i in y:
                url = self.get_wg_check_url(x,i)
                UrlList.append(url)

        data = self.check_weblogic(UrlList, processes=20)
        return {"recode": 0, "redata": data}

    def check_all_weblogic_interface(self):
        '''检查全部服务'''

        UrlList = []
        group_all = conf_data("app_group")
        for group in group_all:
            for host in group_all.get(group):
                for port in group_all.get(group).get(host):
                    url = self.get_wg_check_url(host,port)
                    UrlList.append(url)

        data = self.check_weblogic(UrlList, processes=80)
        return {"recode": 0, "redata": data}
