#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"
req_url = app_url + "/api/v2/host"

json_headers = {"content-type": "application/json"}


class HostTask(object):
    """docstring for HostTask"""
    def __init__(self, ip):
        super(HostTask, self).__init__()
        self.ip = ip

    def post(self, content):
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": content
        }
        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def cmd(self, body):
        print(f">>HostTask cmd: {body}")
        content = {
            "task": "shell",
            "ip": self.ip,
            "user": "ngca",
            "arg": body
        }
        self.post(content)

    def unit(self, body):
        print(f">>HostTask unit: {body}")
        content = {
            "task": "unit",
            "ip": self.ip,
            "user": "ngca",
            "arg": body
        }
        self.post(content)

    def script(self, body):
        print(f">>HostTask script: {body}")
        content = {
            "task": "script",
            "ip": self.ip,
            "user": "ngca",
            "arg": body
        }
        self.post(content)

h1 = HostTask('10.2.1.67')
# h1.cmd('uptime')
# h1.cmd('hostname')

# h1.unit('uptime')
# h1.unit('disk')
# h1.unit('mem')
# h1.unit('netss')
# h1.unit('netrxtx')
# h1.unit('netlistening')
# h1.unit('cpu')
# h1.unit('vmstat')

h1.script('~/f1.sh')

