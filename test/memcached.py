#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"
service_url = app_url + "/api/v2/service"

json_headers = {"content-type": "application/json"}


class MemCachedManager(object):
    """docstring for MemCachedManager"""

    def __init__(self, ip, port):
        super(MemCachedManager, self).__init__()
        self.ip = ip
        self.port = port

    def post(self, task):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": task,
                "unit": "memcached",
                "server": self.ip,
                "port": self.port
                }
        }

        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print(">> MemCachedManager %s" % task)
        print("http status--------->> %s" % r.status_code)
        print(r.text)


    def set(self, key, value):
        print(">> MemCachedManager set  %s" % key)
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": "set",
                "unit": "memcached",
                "server": self.ip,
                "port": self.port,
                "key": key,
                "value": value
                }
        }

        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print(">> MemCachedManager %s" % "set")
        print("http status--------->> %s" % r.status_code)
        print(r.text)


    def get(self, key):
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {
                "task": "get",
                "unit": "memcached",
                "server": self.ip,
                "port": self.port,
                "key": key
                }
        }

        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print(">> MemCachedManager %s" % "get")
        print("http status--------->> %s" % r.status_code)
        print(r.text)


mc = MemCachedManager("10.2.1.67", '21101')
# mc.post('start')
# mc.post('stop')
# mc.post('reboot')
# mc.post('link_sum')


mc.get("name")
mc.post('cleardata')
mc.get("name")
mc.set("name","chenwx")
