#!/usr/bin/python
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2018-02-23 22:59:57
__author__ = 'chenwx'

import socket
import sys

def port_scan(ip,port):
    socket.setdefaulttimeout(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip, int(port)))
    print(result)

if len(sys.argv) < 2:
    sys.exit(1)

ip = sys.argv[1]
port = sys.argv[2]
port_scan(ip,port)
