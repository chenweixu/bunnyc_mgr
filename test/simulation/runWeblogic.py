#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2019-08-06 12:12:13
__author__ = 'chenwx'

import SimpleHTTPServer
import SocketServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class MyHttpHadnle(SimpleHTTPRequestHandler):
    """docstring for MyHttpHadnle"""
    def do_GET(self):
        buf = 'chenwx'
        self.protocal_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Welcome", "Contect")
        self.end_headers()
        self.wfile.write(buf)

PORT = 17101
httpd = SocketServer.TCPServer(("", PORT), MyHttpHadnle)

print "serving at port", PORT
httpd.serve_forever()
