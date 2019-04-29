#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"
host_url = app_url + "/api/v2/monitor"

json_headers = {"content-type": "application/json"}


class MonitorData(object):
    """docstring for MonitorData"""

    def __init__(self):
        super(MonitorData, self).__init__()

    def post(self, unit):
        mess = {
            "key": "c1c2",
            "obj": "monitor",
            "content": {"unit": unit, "ip": "10.2.1.2", "type": 'host'},
        }

        r = requests.post(host_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def uptime(self):
        print(">>MonitorData system info: uptime")
        self.post("uptime")



showhost = MonitorData()
showhost.uptime()
