#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2019-08-08 21:00:55
__author__ = 'chenwx'

import json
import requests

app_url = "http://127.0.0.1:9002"

req_url = app_url + "/api/v2/sms"


def send_sms(phone, body):
    r = requests.get(req_url, timeout=10, params={"phone": phone, "body": body})
    print("http status--------->> %s" % r.status_code)
    a = r.text
    print(a)
    return r.status_code


# send_sms('15000000001', '服务器故障')
send_sms('15000000001,15000000002', '服务器又故障')
