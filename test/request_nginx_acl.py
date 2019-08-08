#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"

req_url = app_url + "/api/v3/nginx"

json_headers = {"content-type": "application/json"}

class Nginx(object):
    """docstring for Nginx"""

    def __init__(self):
        super(Nginx, self).__init__()

    def post(self, mess):
        r = requests.post(req_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def lock(self, iplist):
        mess = {
            "obj": "dmz_nginx",
            "task": "lock",
            "ip": iplist
        }
        self.post(mess)

    def unlock(self, iplist):
        mess = {
            "obj": "dmz_nginx",
            "task": "unlock",
            "ip": iplist
        }
        self.post(mess)

    def clearlock(self):
        mess = {
            "obj": "dmz_nginx",
            "task": "clearlock",
        }
        self.post(mess)

    def showlock(self):
        mess = {
            "obj": "dmz_nginx",
            "task": "showlock",
        }
        self.post(mess)


nginx = Nginx()
# nginx.lock(['10.2.1.99'])
nginx.lock(['211.2.1.99'])
# nginx.lock(['10.2.1.99','2.1.3.4'])
# nginx.unlock(['10.2.1.99'])
# nginx.unlock(['211.2.1.99'])

nginx.showlock()
# nginx.clearlock()
# nginx.showlock()
