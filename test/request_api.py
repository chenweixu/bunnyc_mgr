#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://10.2.1.5:9002"

host_url = app_url + "/api/v2/host"
network_url = app_url + "/api/v2/network"
service_url = app_url + "/api/v2/service"
checkweburl_url = app_url + "/api/v1/checkweburl"

json_headers = {"content-type": "application/json"}


class checl_web_url(object):
    """docstring for checl_web_url"""

    def __init__(self):
        super(checl_web_url, self).__init__()

    def get_url_status(self, checkurl):
        mess = {"url": checkurl}
        print(">> get_url_status %s" % checkurl)
        r = requests.get(checkweburl_url, params=mess)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

web = checl_web_url()
web.get_url_status('http://www.baidu.com')
# web.get_url_status('http://10.21.43.2')
