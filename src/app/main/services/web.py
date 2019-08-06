import requests
from multiprocessing import Pool
from app import work_log

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

