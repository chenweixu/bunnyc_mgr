# 2018-09-18 11:11:39
# Version: 0.1
# opsmgr

# docker build -t chenwx/bmgr_platform:0.1 -f conf/bmgr_platform.dockerfile .

FROM chenwx/python:3
MAINTAINER chenwx "chenwx716@163.com"

RUN apk add --no-cache py3-paramiko py3-cffi py3-cryptography

ADD requirements.txt /usr/local/requirements.txt

# install python pkg
RUN pip3 install --upgrade pip \
    && pip3 install -r /usr/local/requirements.txt \
    && rm /usr/local/requirements.txt
