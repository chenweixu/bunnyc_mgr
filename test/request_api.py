#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2017-07-09 18:26:45
__author__ = "chenwx"

import json
import requests

app_url = "http://10.2.1.5:9002"

host_url = app_url + "/api/v2/host"
hostcmd_url = app_url + "/api/v1/hostcmd"
network_url = app_url + "/api/v1/network"
weblogic_url = app_url + "/api/v1/weblogic"
nginx_url = app_url + "/api/v1/nginx"
checkweburl_url = app_url + "/api/v1/checkweburl"
memcached_url = app_url + "/api/v1/memcached"

json_headers = {"content-type": "application/json"}


class ShowSysTemInfo(object):
    """docstring for ShowSysTemInfo"""

    def __init__(self):
        super(ShowSysTemInfo, self).__init__()

    def post(self, unit):
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {
                "task": "remote", "ip": "10.2.1.67", "unit": unit
            }
        }
        r = requests.post(
            host_url, data=json.dumps(mess), headers=json_headers
        )
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def disk(self):
        print(">>ShowSysTemInfo system info: disk")
        self.post('disk')

    def mem(self):
        print(">>ShowSysTemInfo system info: mem")
        self.post('mem')

    def netlistening(self):
        print(">>ShowSysTemInfo system info: netlist")
        self.post('netlistening')

    def netss(self):
        print(">>ShowSysTemInfo system info: netss")
        self.post('netss')

    def uptime(self):
        print(">>ShowSysTemInfo system info: uptime")
        self.post('uptime')

    def netrxtx(self):
        print(">>ShowSysTemInfo system info: netrxtx")
        self.post('netrxtx')

    def vmstat(self):
        print(">>ShowSysTemInfo system info: vmstart")
        self.post('vmstat')

    def cpu(self):
        print(">>ShowSysTemInfo system info: cpu")
        self.post('cpu')


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
            "content": {
                "task": "remote", "ip": "10.2.1.67", "cmd": "uptime"
            }
        }
        self.post(mess)

    def nowait(self):
        print(">> HostManagerhostcmd no wait user network cmd: uptime")
        mess = {
            "key": "c1c2",
            "obj": "host",
            "content": {
                "task": "remote", "ip": "10.2.1.67", "cmd": "uptime", "user": "weblogic"
            }
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
        r = requests.get(network_url, timeout=5, params={"host": ip})
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def check_local_port(self, port):
        mess = {
            "sip": "127.0.0.1",
            "ip": "10.2.1.5",
            "port": port,
            "task": "check_port",
        }
        print(
            ">> Network check sip-> %s , ip-> %s ,port-> %s"
            % ("127.0.0.1", mess.get("ip"), str(port))
        )
        r = requests.post(network_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)
        return r.status_code

    def check_server_login_port(self, port):
        mess = {
            "sip": "10.2.1.67",
            "ip": "10.2.1.5",
            "port": port,
            "task": "check_port",
        }
        print(
            ">> Network check sip-> %s , ip-> %s ,port-> %s"
            % ("10.2.1.67", mess.get("ip"), str(port))
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
        r = requests.post(nginx_url, data=json.dumps(mess), headers=json_headers)
        print("http status--------->> %s" % r.status_code)
        print(r.text)

    def start_nginx(self, ip):
        print(">> start_nginx  %s" % ip)
        self.post({"webserver": ip, "task": "start"})

    def lock_ip(self, ip):
        print(">> lock_ip  %s" % ip)
        self.post({"lock_ip": ip, "task": "lock"})

    def stop_nginx(self, ip):
        print(">> stop_nginx  %s" % ip)
        self.post({"webserver": ip, "task": "stop"})

    def restart(self, ip):
        print(">> restart  %s" % ip)
        self.post({"webserver": ip, "task": "restart"})

    def show_access_log(self, ip):
        print(">> show_access_log  %s" % ip)
        self.post({"webserver": ip, "task": "show_access_log"})

    def show_error_log(self, ip):
        print(">> show_error_log  %s" % ip)
        self.post({"webserver": ip, "task": "show_error_log"})

    def clear_access_log(self, ip):
        print(">> clear_access_log  %s" % ip)
        self.post({"webserver": ip, "task": "clear_access_log"})


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

hostcmd = HostManagerhostcmd()
hostcmd.uptime()
hostcmd.nowait()

# netcheck = Network()
# netcheck.pinghost('10.2.1.5')
# netcheck.pinghost('10.2.1.68')
# netcheck.pinghost('10.23.12.68')
# netcheck.check_local_port(9002)
# netcheck.check_server_login_port(9002)
# netcheck.check_server_login_port(8000)

# weblogic = ServiceManagerWeblogic()
# weblogic.start_weblogic_single_service()
# weblogic.start_weblogic_single_host()
# weblogic.stop_weblogic_single_service()
# weblogic.stop_weblogic_single_host()
# weblogic.show_access_log()
# weblogic.show_error_log()
# weblogic.start_group()
# weblogic.stop_group()

# nginx = Nginx()
# nginx.start_nginx('10.2.1.67')
# nginx.start_nginx('10.2.1.68')
# nginx.lock_ip('3.1.1.4')
# nginx.restart('10.2.1.67')
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
