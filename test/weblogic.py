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

class WeblogicOne(object):
    """docstring for WeblogicOne"""
    def __init__(self, ip, port):
        super(WeblogicOne, self).__init__()
        self.ip = ip
        self.port = port

    def run_task(self,task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": task,
                "unit": "weblogic",
                "server": self.ip,
                "port": self.port
                }
        }
        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print("http status------task: %s --->> %s" % (task,r.status_code))
        print(r.text)


class WeblogicHost(object):
    """docstring for WeblogicHost"""
    def __init__(self, ip):
        super(WeblogicHost, self).__init__()
        self.ip = ip

    def run_task(self,task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": task,
                "unit": "weblogic",
                "server": self.ip,
                }
        }
        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print("http status------task: %s --->> %s" % (task,r.status_code))
        print(r.text)


class WenlogicGroup(object):
    """docstring for WenlogicGroup"""
    def __init__(self, group):
        super(WenlogicGroup, self).__init__()
        self.group = group

    def run_task(self,task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": task,
                "unit": "weblogic",
                "group": self.group,
                }
        }
        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print("http status------task: %s --->> %s" % (task,r.status_code))
        print(r.text)


w1 = WeblogicOne('10.2.1.67', 17101)
w1.run_task('start')
w1.run_task('stop')
w1.run_task('reboot')
w1.run_task('accesslog')
w1.run_task('projectlog')
w1.run_task('check')

# w2 = WeblogicHost('10.2.1.67')
# w2.run_task('start')
# w2.run_task('stop')
# w2.run_task('reboot')
# w2.run_task('check')

# w3 = WenlogicGroup("dmz1")
# w3.run_task('start')
# w3.run_task('stop')
# w3.run_task('reboot')
# w3.run_task('check')