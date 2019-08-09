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


class MemcachedOne(object):
    """docstring for MemcachedOne"""

    def __init__(self, ip, port=None):
        super(MemcachedOne, self).__init__()
        self.ip = ip
        self.port = port

    def run_task(self, task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "unit": "memcached",
                "types": 'single',
                "task": task,
                "server": self.ip,
                "port": self.port,
            },
        }
        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status------task: %s --->> %s" % (task, r.status_code))
        print(r.text)


class MemcachedGroup(object):
    """docstring for MemcachedGroup"""

    def __init__(self, group):
        super(MemcachedGroup, self).__init__()
        self.group = group

    def run_task(self, task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "unit": "memcached",
                "types": 'group',
                "task": task,
                "group": self.group
            },
        }
        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status------task: %s --->> %s" % (task, r.status_code))
        print(r.text)


# w1 = MemcachedOne("10.2.1.67", 21101)
# w1.run_task('start')
# w1.run_task('stop')

w3 = MemcachedGroup("test")
# w3.run_task('start')
# w3.run_task('stop')

