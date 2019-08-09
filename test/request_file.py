#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://127.0.0.1:9002"

file_get_url = app_url+"/api/v2/downfile/"
file_down_url = app_url+"/api/v2/downfile"
file_upload_url = app_url+"/api/v2/upload"


json_headers = {"content-type": "application/json"}


class file(object):
    """docstring for file"""
    def __init__(self):
        super(file, self).__init__()

    def get_file(self, filename):
        url = file_get_url+str(filename)
        print(url)
        data = requests.get(url)
        with open(url.split('/')[-1], "wb") as code:
            code.write(data.content)
            print('down file testdownfile.log --- yes')

    def down_file(self, ip, user, file_url):
        mess = {
            "key": "c1c2",
            "obj": "file",
            "content": {"task": "remote_file_down", "ip": ip, "file": file_url, "user": user},
        }
        r = requests.post(file_down_url, data=json.dumps(mess), headers=json_headers)
        print(r.text)

    def upload(self, ip, user, file_url):
        mess = {
        }
        r = requests.post(file_down_url, data=json.dumps(mess), headers=json_headers)


task = file()
# task.get_file('testdownfile.log')
task.down_file('10.2.1.67', 'ngca', '/home/ngca/local_service.sh')
