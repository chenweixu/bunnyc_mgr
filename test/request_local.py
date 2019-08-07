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

    def post(self, content):
        mess = {
            "key": "c1c2",
            "obj": "local",
            "content": content
        }

        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)


    def cmd(self, body):
        content = {
            "task": "cmd",
            "arg": body
        }
        self.post(content)

    def unit(self, body):
        content = {
            "task": "unit",
            "arg": body
        }
        self.post(content)

    def srcipt(self, file):
        content = {
            "task": "script",
            "arg": file
        }
        self.post(content)


task = ShowLocal()
task.cmd('ls /tmp')
task.cmd('uptime')
task.cmd('df -h')

task.unit('disk')
task.unit('disk_dict')
task.unit('uptime')
task.unit('uptime_dict')
task.unit('cpu')
task.unit('mem_dict')

task.srcipt('/home/wait/code/f1.sh')
