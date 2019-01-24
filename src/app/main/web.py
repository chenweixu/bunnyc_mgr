import requests
from app.main.conf import conf_data
from app.main.util.mylog import My_log
from multiprocessing import Pool

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class CheckWebInterface(object):
    """docstring for CheckWebInterface"""

    def __init__(self):
        super(CheckWebInterface, self).__init__()

    def get_url_status_code(self, url, timeout=2):
        try:
            r = requests.get(url, timeout=timeout)
            code = r.status_code
            r.close()
            return code
        except Exception as e:
            work_log.error("get_url_status_code error: %s" % url)
            work_log.error(str(e))
            return 509

    def get_nginx_status(self, url, timeout=2):
        try:
            r = requests.get(url, timeout=timeout)
            txt = r.text
            r.close()
            return txt
        except Exception as e:
            work_log.error(str(e))
            return False

    def get_active_connections(self, url):
        txt = self.get_nginx_status(url)
        if not txt:
            connections = 999
        else:
            connections = int(txt.split("\n")[0].split(":")[1])
        return (url, connections)

    def get_group_active_connections(self, url_list):
        data = []
        for url in url_list:
            data.append(self.get_active_connections(url))
        return data

    def show_nginx_status(self, host):
        url = "http://" + host + ":18001/nginx_status"
        return self.get_nginx_status(url)

    def check_web_group(self, url_list):
        new_list = []
        for url in url_list:
            code = self.get_url_status_code(url)
            new_list.append((url, code))
        return new_list

    def check_weblogic_service(self, url):
        host = url.split(":")[1].lstrip("//")
        port = url.split(":")[2].split("/")[0]
        req_url = url.split(":")[2].lstrip(port)
        req_code = self.get_url_status_code(url)
        if req_code == 200:
            status = "ok"
        else:
            status = "error"
        return (host, port, req_url, req_code, status)

    def get_task_all(self):
        app_list = conf_data("app_group")
        interface = conf_data("service_info", "weblogic", "weblogic_interface")
        task = []
        for group in app_list:
            for host in app_list.get(group):
                for port in app_list.get(group).get(host):
                    url = "http://" + host + ":" + port + interface
                    task.append(url)
        return task

    def get_task_group(self, grou_name):
        info = conf_data("app_group", grou_name)
        interface = conf_data("service_info", "weblogic", "weblogic_interface")
        task = []
        for host in info:
            for port in info.get(host):
                url = "http://" + host + ":" + port + interface
                task.append(url)
        return task

    def work_start(self, group=None):
        if not group:
            task = self.get_task_all()
            pool = Pool(processes=30)
            result = []
            for url in task:
                result.append(pool.apply_async(self.check_weblogic_service, (url,)))
            pool.close()
            pool.join()

            Display = []
            for res in result:
                vle = res.get()
                if vle != 0:
                    Display.append(vle)
            return Display
        else:
            task = self.get_task_group(group)
            pool = Pool(processes=30)
            result = []
            for url in task:
                result.append(pool.apply_async(self.check_weblogic_service, (url,)))
            pool.close()
            pool.join()

            Display = []
            for res in result:
                vle = res.get()
                if vle != 0:
                    Display.append(vle)
            return Display
