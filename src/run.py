#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2018-08-04 21:19:45
__author__ = 'chenwx'

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9002)
    # app.run(debug=False, host='0.0.0.0', port=9002)
