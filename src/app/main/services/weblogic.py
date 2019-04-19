import itertools
from multiprocessing import Pool
from app.main.conf import conf_data
from app.utils.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.hostshell import HostGroupCmd
from app.main.services.web import CheckWebInterface

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()

class WeblogicManagerSingle(object):
    """docstring for WeblogicManagerSingle"""
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
        # 启动单个服务
        work_log.debug('start_weblogic_single_service')
        if not port:
            cmd = ' '.join([self.service_script, 'weblogic', 'start', str(int(self.port) - 17100)])
        else:
            cmd = ' '.join([self.service_script, 'weblogic', 'start', str(int(port) - 17100)])
        work_log.debug(str(cmd))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}


    def stop_weblogic_single_service(self, port=None):
        # 停止单个服务
        if not port:
            cmd = ' '.join([self.service_script, 'weblogic', 'stop', str(int(self.port) - 17100)])
        else:
            cmd = ' '.join([self.service_script, 'weblogic', 'stop', str(int(port) - 17100)])
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": 0, "redata": "success"}
        else:
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
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}


    def showprojectlog(self):
        log_out = conf_data("service_info", "weblogic", "log_out")
        cmd = "tail -n 500 " + log_out.replace("1", str(int(self.port) - 17100))
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}

    def start_wg_single(self):
        # 并行 启动单个主机上的6个服务
        cmd = ' '.join([self.service_script, 'weblogic', 'start_group'])
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}


    def stop_wg_single(self):
        # 并行 停止单个主机上的6个服务
        cmd = ' '.join([self.service_script, 'weblogic', 'stop_group'])
        run_data = self._weblogic_ssh_cmd(cmd)
        if run_data[0] == 0:
            return {"recode": run_data[0], "redata": run_data[1]}
        else:
            return {"recode": run_data[0], "redata": run_data[1]}


    def run_task(self, task):
        work_log.info('weblogic service task: %s , host: %s port: %s' % (task, self.ip, self.port))
        if self.port and int(self.port) >= 17101 and int(self.port) <= 17106:
            try:
                if task == "start":
                    return self.start_weblogic_single_service()
                elif task == "stop":
                    return self.stop_weblogic_single_service()
                elif task == "reboot":
                    return self.reboot_weblogic_single_service()
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
                elif task == "check":
                    pass
                else:
                    return {"recode": 4, "redata": '不支持该操作'}
            except Exception as e:
                work_log.error("single weblogic service run error")
                work_log.error(str(e))
                return {"recode": 2, "redata": str(e)}

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

    # def start_weblogic_single_service(ip, serid):
    #     server = WeblogicManagerSingle(ip, serid)
    #     server.start_weblogic_single_service()

    def start_single_host(self, ip):
        server = WeblogicManagerSingle(ip)
        server.start_wg_single()

    def stop_single_host(self, ip):
        server = WeblogicManagerSingle(ip)
        server.stop_wg_single()

    def start_wg_group(self, group_name):
        host_list = self.get_group_host(group_name)
        info = []
        pool = Pool(processes=10)

        for ip in host_list:
            info.append(pool.apply_async(self.start_single_host, (ip,)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data

    def stop_wg_group(self, group_name):
        host_list = self.get_group_host(group_name)
        info = []
        pool = Pool(processes=10)

        for ip in host_list:
            info.append(pool.apply_async(self.stop_single_host, (ip,)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data


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

