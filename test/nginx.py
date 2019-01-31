#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://10.2.1.5:9002"

service_url = app_url + "/api/v2/service"

json_headers = {"content-type": "application/json"}

class Nginx(object):
    """docstring for Nginx"""

    def __init__(self):
        super(Nginx, self).__init__()

    def post(self, mess):
        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def single_nginx(self, ip, task):
        print(">> single_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": task, "unit": "nginx", "server": ip},
        }
        self.post(mess)

    def lock_nginx(self, task, ip=None):
        print(">> lock_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": task, "unit": "nginx", "ip": ip},
        }
        self.post(mess)

    def show_lock(self):
        print(">> show_lock ")
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": "showlock", "unit": "nginx"}
        }
        self.post(mess)



nginx = Nginx()
nginx.single_nginx("10.2.1.67", "start")
nginx.single_nginx("10.2.1.67", "stop")
nginx.single_nginx("10.2.1.67", "reload")
nginx.single_nginx("10.2.1.67", "restart")
nginx.single_nginx("10.2.1.67", "show_access_log")
nginx.single_nginx("10.2.1.67", "show_error_log")
nginx.single_nginx("10.2.1.67", "clear_access_log")

nginx.lock_nginx("lock", '3.1.1.9')
nginx.show_lock()

nginx.restart('10.2.1.68')
nginx.stop_nginx('10.2.1.67')
nginx.stop_nginx('10.2.1.68')

nginx.show_access_log('10.2.1.68')
nginx.show_error_log('10.2.1.68')
nginx.clear_access_log('10.2.1.68')
