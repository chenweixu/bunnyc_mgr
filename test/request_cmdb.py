#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2019-04-03 10:50:04
__author__ = 'chenwx'

import json
import requests
import random

app_url = "http://127.0.0.1:9002"

req_url = app_url + "/api/v2/cmdb/host"

json_headers = {"content-type": "application/json"}

class CmdbHost(object):
    """docstring for CmdbHost"""

    def __init__(self):
        super(CmdbHost, self).__init__()

    def add(self, body):
        mess = {
            "key": "c1c2",
            "obj": "cmdb",
            "content": {
                "task": 'add',
                "unit": "host",
                "body": body
                }
        }

        r = requests.post(req_url,data=json.dumps(mess),
                headers=json_headers, timeout=5)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def update(self,id,body):
        body['id'] = id
        mess = {
            "key": "c1c2",
            "obj": "cmdb",
            "content": {
                "task": 'update',
                "unit": "host",
                "body": body
                }
        }

        r = requests.post(req_url,data=json.dumps(mess),
                headers=json_headers, timeout=5)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def delhost(self,hostid):
        mess = {
            "key": "c1c2",
            "obj": "cmdb",
            "content": {
                "task": 'del',
                "unit": "host",
                "id": hostid
                }
        }

        r = requests.post(req_url,data=json.dumps(mess),
                headers=json_headers, timeout=5)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def show(self,ip):
        mess = {
            "key": "c1c2",
            "obj": "cmdb",
            "content": {
                "task": 'show',
                "unit": "host",
                "ip": ip
                }
        }

        r = requests.post(req_url,data=json.dumps(mess),
                headers=json_headers, timeout=5)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def showall(self):
        mess = {
            "key": "c1c2",
            "obj": "cmdb",
            "content": {
                "task": 'showall',
                "unit": "host",
                }
        }

        r = requests.post(req_url,data=json.dumps(mess),
                headers=json_headers, timeout=5)
        print("http status--------->> %s" % r.status_code)
        print(r.text)



data = {
    'ip_v4': '10.2.1.'+str(random.randint(1,200)),
    'ip_v6': '2409:2079:1610:6010:7001:0000:0000:0116',
    'ip_v4_m': '192.168.1.'+str(random.randint(1,200)),
    'name': 'test1',
    'operating_system': 'fedora29',
    'hostname': 'myhost',
    'cpu_number': '4',
    'memory_size': '11917',
    'sn': '31dihewihf'+str(random.randint(1,30000)),
    'address': '北京市亦庄联通机房',
    'belong_machineroom': '5019',
    'rack': 'A18',
    'manufacturer': 'HP',
    'type': 'PC',
    'dev_category': 'WEB',
    'produce': '0',
    'level': '2',
    'info': '这是一段备注信息'
}

host = CmdbHost()
# host.add(data)

# host.delhost(3)
# host.update(22,data)
# host.show('10.2.1.126')
host.showall()

