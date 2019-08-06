#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2019-08-06 22:08:14
__author__ = 'chenwx'

import json
import requests

app_url = "http://127.0.0.1:9002"
req_url = app_url + "/api/v2/local"

json_headers = {"content-type": "application/json"}

class ShowLocal(object):
    """docstring for ShowLocal"""
    def __init__(self):
        super(ShowLocal, self).__init__()
        self.mess = {
            "key": "c1c2",
            "obj": "local"
        }

    def post(self, content):
        self.mess["content"] = content
        print(self.mess)
        r = requests.post(req_url, data=json.dumps(self.mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)


    def cmd(self, body):
        body = {
            "task": "cmd",
            "cmd": body
        }
        self.post(body)

    def unit(self, body):
        body = {
            "task": "unit",
            "unit": body
        }
        self.post(body)

    def srcipt(self, file):
        body = {
            "task": "script",
            "file": file
        }
        self.post(body)


task = ShowLocal()
task.cmd('ls /tmp')
task.cmd('uptime')
task.cmd('df -h')

task.unit('disk')
task.unit('diskinfo')
task.unit('uptime')
task.unit('uptime_dict')
task.unit('cpu')
task.unit('meminfo')

task.srcipt('/home/wait/code/f1.sh')
