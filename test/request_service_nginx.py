#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"

req_url = app_url + "/api/v2/service"

json_headers = {"content-type": "application/json"}

class Nginx(object):
    """docstring for Nginx"""

    def __init__(self):
        super(Nginx, self).__init__()

    def post(self, mess):
        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def single_nginx(self, ip, task):
        print(">> single_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"types": "single", "task": task, "unit": "nginx", "server": ip},
        }
        self.post(mess)

    def lock(self, task, ip=None):
        print(">> lock_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"types": "lock", "task": task, "unit": "nginx", "ip": ip},
        }
        self.post(mess)

nginx = Nginx()
# nginx.single_nginx("10.2.1.67", "stop")
# nginx.single_nginx("10.2.1.67", "start")
# nginx.single_nginx("10.2.1.68", "start")
# nginx.single_nginx("10.2.1.67", "reload")
# nginx.single_nginx("10.2.1.67", "restart")
# nginx.single_nginx("10.2.1.67", "show_access_log")
# nginx.single_nginx("10.2.1.67", "show_error_log")
# nginx.single_nginx("10.2.1.67", "clear_access_log")


# nginx.single_nginx("10.2.1.67", "start")
# nginx.single_nginx("10.2.1.68", "start")

# nginx.lock("lock", '3.1.1.9')
# nginx.lock("lock", '211.2.1.99')
# nginx.lock("unlock", '3.1.1.9')
# nginx.lock("unlock", '211.2.1.99')
# nginx.lock('showlock')
# nginx.lock('clearlock')
# nginx.lock('showlock')
