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


class ShowSysTemInfo(object):
    """docstring for ShowSysTemInfo"""

    def __init__(self):
        super(ShowSysTemInfo, self).__init__()

    def post(self, unit):
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {"task": "remote", "ip": "10.2.1.67", "unit": unit},
        }
        r = requests.post(host_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def disk(self):
        print(">>ShowSysTemInfo system info: disk")
        self.post("disk")

    def mem(self):
        print(">>ShowSysTemInfo system info: mem")
        self.post("mem")

    def netlistening(self):
        print(">>ShowSysTemInfo system info: netlist")
        self.post("netlistening")

    def netss(self):
        print(">>ShowSysTemInfo system info: netss")
        self.post("netss")

    def uptime(self):
        print(">>ShowSysTemInfo system info: uptime")
        self.post("uptime")

    def netrxtx(self):
        print(">>ShowSysTemInfo system info: netrxtx")
        self.post("netrxtx")

    def vmstat(self):
        print(">>ShowSysTemInfo system info: vmstart")
        self.post("vmstat")

    def cpu(self):
        print(">>ShowSysTemInfo system info: cpu")
        self.post("cpu")


class HostManagerhostcmd(object):
    """docstring for HostManagerhostcmd"""

    def __init__(self):
        super(HostManagerhostcmd, self).__init__()

    def post(self, mess):
        r = requests.post(host_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def uptime(self):
        print(">> HostManagerhostcmd wait user network cmd: uptime")
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {"task": "remote", "ip": "10.2.1.67", "cmd": "uptime"},
        }
        self.post(mess)

    def nowait(self):
        print(">> HostManagerhostcmd no wait user network cmd: uptime")
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {
                "task": "remote",
                "ip": "10.2.1.67",
                "cmd": "uptime",
                "user": "weblogic",
            },
        }

        recode = self.post(mess)
        if recode == 403:
            print("http status--------->> yes")


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


class ServiceManagerWeblogic(object):
    """docstring for ServiceManagerWeblogic"""

    def __init__(self):
        super(ServiceManagerWeblogic, self).__init__()

    def get(self, mess):
        r = requests.get(weblogic_url, params=mess)
        # r = requests.get(weblogic_url, timeout=5,params=mess)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def start_weblogic_single_service(self):
        mess = {"task": "start", "service_number": 1, "hosts": "10.2.1.67"}
        print(">> start_weblogic_single_service host %s" % mess.get("hosts"))
        self.get(mess)

    def stop_weblogic_single_service(self):
        mess = {"task": "stop", "service_number": 1, "hosts": "10.2.1.67"}
        print(">> stop_weblogic_single_service host %s" % mess.get("hosts"))
        self.get(mess)

    def start_weblogic_single_host(self):
        mess = {"task": "start", "service_number": "all", "hosts": "10.2.1.67"}
        print(">> start_weblogic_single_host host %s" % mess.get("hosts"))
        self.get(mess)

    def stop_weblogic_single_host(self):
        mess = {"task": "stop", "service_number": "all", "hosts": "10.2.1.67"}
        print(">> stop_weblogic_single_host host %s" % mess.get("hosts"))
        self.get(mess)

    def show_access_log(self):
        mess = {"task": "show_access_log", "service_number": 1, "hosts": "10.2.1.67"}
        print(">> show_access_log host %s" % mess.get("hosts"))
        self.get(mess)

    def show_error_log(self):
        mess = {"task": "show_error_log", "service_number": 1, "hosts": "10.2.1.67"}
        print(">> show_error_log host %s" % mess.get("hosts"))
        self.get(mess)

    def start_group(self):
        mess = {"task": "start_group", "group_number": "dmz1"}
        print(">> start_group group_number %s" % mess.get("group_number"))
        self.get(mess)

    def stop_group(self):
        mess = {"task": "stop_group", "group_number": "dmz1"}
        print(">> stop_group group_number %s" % mess.get("group_number"))
        self.get(mess)


class Nginx(object):
    """docstring for Nginx"""

    def __init__(self):
        super(Nginx, self).__init__()

    def post(self, mess):
        r = requests.post(service_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def single_nginx(self, ip, task):
        print(">> single_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": task, "unit": "nginx", "server": ip},
        }
        self.post(mess)

    def lock_nginx(self, task, ip=None):
        print(">> lock_nginx  %s task: %s" % (ip, task))
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": task, "unit": "nginx", "ip": ip},
        }
        self.post(mess)

    def show_lock(self):
        print(">> show_lock ")
        mess = {
            "key": "c1c2",
            "obj": "service",
            "content": {"task": "showlock", "unit": "nginx"}
        }
        self.post(mess)


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


class MemCachedManager(object):
    """docstring for MemCachedManager"""

    def __init__(self):
        super(MemCachedManager, self).__init__()

    def post(self, mess):
        r = requests.post(memcached_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def start(self, mc):
        print(">> MemCachedManager start  %s" % mc)
        self.post({"mc_addr": mc, "task": "start"})

    def stop(self, mc):
        print(">> MemCachedManager stop  %s" % mc)
        self.post({"mc_addr": mc, "task": "stop"})

    def reboot(self, mc):
        print(">> MemCachedManager reboot  %s" % mc)
        self.post({"mc_addr": mc, "task": "reboot"})

    def set(self, mc):
        print(">> MemCachedManager set  %s" % mc)
        self.post(
            {
                "mc_addr": mc,
                "task": "set",
                "mc_key": "myname",
                "mc_value": "chenwx",
                "mc_expire": "30",
            }
        )

    def get(self, mc):
        print(">> MemCachedManager get  %s" % mc)
        self.post({"mc_addr": mc, "task": "get", "mc_key": "myname"})

    def link_sum(self, mc):
        print(">> MemCachedManager link_sum  %s" % mc)
        self.post({"mc_addr": mc, "task": "link_sum"})


# showhost = ShowSysTemInfo()
# showhost.disk()
# showhost.mem()
# showhost.netlistening()
# showhost.netss()
# showhost.uptime()
# showhost.netrxtx()
# showhost.vmstat()
# showhost.cpu()

# hostcmd = HostManagerhostcmd()
# hostcmd.uptime()
# hostcmd.nowait()

# netcheck = Network()
# netcheck.pinghost('10.2.1.5')
# netcheck.pinghost('10.2.1.67')
# netcheck.pinghost('10.23.12.68')
# netcheck.check_local_port("10.2.1.5", 9002)
# netcheck.check_local_port("10.2.1.5", 9002, source="10.2.1.67")
# netcheck.check_local_port("10.2.1.5", 22, source="10.2.1.67")


# weblogic = ServiceManagerWeblogic()
# weblogic.start_weblogic_single_service()
# weblogic.start_weblogic_single_host()
# weblogic.stop_weblogic_single_service()
# weblogic.stop_weblogic_single_host()
# weblogic.show_access_log()
# weblogic.show_error_log()
# weblogic.start_group()
# weblogic.stop_group()

nginx = Nginx()
# nginx.single_nginx("10.2.1.67", "start")
# nginx.single_nginx("10.2.1.67", "stop")
# nginx.single_nginx("10.2.1.67", "reload")
# nginx.single_nginx("10.2.1.67", "restart")
# nginx.single_nginx("10.2.1.67", "show_access_log")
# nginx.single_nginx("10.2.1.67", "show_error_log")
# nginx.single_nginx("10.2.1.67", "clear_access_log")

nginx.lock_nginx("lock", '3.1.1.9')
nginx.show_lock()

# nginx.restart('10.2.1.68')
# nginx.stop_nginx('10.2.1.67')
# nginx.stop_nginx('10.2.1.68')

# nginx.show_access_log('10.2.1.68')
# nginx.show_error_log('10.2.1.68')
# nginx.clear_access_log('10.2.1.68')

# web = checl_web_url()
# web.get_url_status('http://www.baidu.com')
# web.get_url_status('http://10.21.43.2')

# mc = MemCachedManager()
# mc.stop('10.2.1.67:21101')
# mc.start('10.2.1.67:21101')
# mc.reboot('10.2.1.67:21101')

# mc.get('10.2.1.67:21101')
# mc.set('10.2.1.67:21101')
# mc.get('10.2.1.67:21101')

# mc.link_sum('10.2.1.67:21101')
