#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://10.2.1.5:9002"
host_url = app_url + "/api/v2/host"

json_headers = {"content-type": "application/json"}


class ShowSysTemInfo(object):
    """docstring for ShowSysTemInfo"""

    def __init__(self):
        super(ShowSysTemInfo, self).__init__()

    def post(self, unit):
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {"task": "remote", "ip": "10.2.1.67", "unit": unit},
        }
        r = requests.post(host_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def disk(self):
        print(">>ShowSysTemInfo system info: disk")
        self.post("disk")

    def mem(self):
        print(">>ShowSysTemInfo system info: mem")
        self.post("mem")

    def netlistening(self):
        print(">>ShowSysTemInfo system info: netlist")
        self.post("netlistening")

    def netss(self):
        print(">>ShowSysTemInfo system info: netss")
        self.post("netss")

    def uptime(self):
        print(">>ShowSysTemInfo system info: uptime")
        self.post("uptime")

    def netrxtx(self):
        print(">>ShowSysTemInfo system info: netrxtx")
        self.post("netrxtx")

    def vmstat(self):
        print(">>ShowSysTemInfo system info: vmstart")
        self.post("vmstat")

    def cpu(self):
        print(">>ShowSysTemInfo system info: cpu")
        self.post("cpu")


class HostManagerhostcmd(object):
    """docstring for HostManagerhostcmd"""

    def __init__(self):
        super(HostManagerhostcmd, self).__init__()

    def post(self, mess):
        r = requests.post(host_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def uptime(self):
        print(">> HostManagerhostcmd wait user network cmd: uptime")
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {"task": "remote", "ip": "10.2.1.67", "cmd": "uptime"},
        }
        self.post(mess)

    def nowait(self):
        print(">> HostManagerhostcmd no wait user network cmd: uptime")
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {
                "task": "remote",
                "ip": "10.2.1.67",
                "cmd": "uptime",
                "user": "weblogic",
            },
        }

        recode = self.post(mess)
        if recode == 403:
            print("http status--------->> yes")


showhost = ShowSysTemInfo()
showhost.disk()
showhost.mem()
showhost.netlistening()
showhost.netss()
showhost.uptime()
showhost.netrxtx()
showhost.vmstat()
showhost.cpu()

hostcmd = HostManagerhostcmd()
hostcmd.uptime()
hostcmd.nowait()
