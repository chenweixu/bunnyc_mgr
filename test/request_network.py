#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://10.2.1.5:9002"
network_url = app_url + "/api/v2/network"

json_headers = {"content-type": "application/json"}

class Network(object):
    """docstring for Network"""

    def __init__(self):
        super(Network, self).__init__()

    def pinghost(self, ip):
        print(">> Network test ping host %s" % ip)
        r = requests.get(network_url, timeout=10, params={"host": ip})
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def check_local_port(self, ip, port, source="localhost"):
        mess = {
            "key": "c1c2",
            "obj": "network",
            "content": {"task": "check_port", "ip": ip, "port": port, "source": source},
        }

        print(
            ">> Network check sip-> %s , ip-> %s ,port-> %s" % (source, ip, str(port))
        )
        r = requests.post(network_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code


netcheck = Network()
netcheck.pinghost('10.2.1.5')
netcheck.pinghost('10.2.1.67')
netcheck.pinghost('10.23.12.68')
netcheck.check_local_port("10.2.1.5", 9002)
netcheck.check_local_port("10.2.1.5", 9002, source="10.2.1.67")
netcheck.check_local_port("10.2.1.5", 22, source="10.2.1.67")
