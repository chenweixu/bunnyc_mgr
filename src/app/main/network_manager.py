import re
import subprocess
import telnetlib
import socket
from multiprocessing.dummy import Pool as ThreadPool
from app.main.conf import conf_data
from app.main.util.mylog import My_log

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class NetworkManager(object):
    """docstring for NetworkManager"""

    def __init__(self):
        super(NetworkManager, self).__init__()

    def host_ping_check(self, ip):
        pinghost = subprocess.Popen(
            ["/bin/ping", "-q", "-c", "3", ip],
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:
            out, error = pinghost.communicate(timeout=4)
        except subprocess.TimeoutExpired:
            pinghost.kill()
            work_log.error("pinghost timeout 4s: %s" % ip)
            return 2
        except Exception as e:
            work_log.error("pinghost other error")
            work_log.error(str(e))
            return 999

        if not error:
            data = out.decode("UTF-8")
            re_obj = re.compile("\d+%")
            try:
                packet_loss = int(re_obj.findall(data)[0].rstrip("%"))
            except Exception as e:
                work_log.error(str(e))
                return 901
            work_log.info("host_ping_check yes: %s" % ip)
            return packet_loss
        else:
            work_log.error("ping host error")
            work_log.info("host_ping_check error: %s" % ip)
            work_log.error(str(error))
            return 1

    def host_ping_list(self, ip_list):
        pool = ThreadPool(2)
        f = pool.map(self.host_ping_check, ip_list)
        pool.close()
        pool.join()
        return zip(ip_list, f)

    def port_check(self, ip, port):
        try:
            tn = telnetlib.Telnet(ip, port=port, timeout=3)
            work_log.info("port_check yes")
            work_log.info("desc_host: %s ,port: %s" % (ip, str(port)))
            return 0
        except ConnectionRefusedError:
            work_log.error("port_check error")
            work_log.error("ConnectionRefusedError")
            return 1
        except Exception as e:
            work_log.error("port_check error")
            work_log.error(str(e))
            return 2

    def port_scan(self, ip, port):
        work_log.debug("networkmanager local port_scan: " + str(ip) + " : " + str(port))
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, int(port)))
        work_log.debug("networkmanager local port_scan, recode: " + str(result))
        return result

    def local_ping(self, ip):
        work_log.info("networkmanager ping host: " + str(ip))
        recode = self.host_ping_check(ip)
        if recode == 0:
            redata = '成功'
        elif recode == 901:
            redata = '服务器端解析错误'
        else:
            redata = "失败"
        data = {"recode": recode, "redata": redata}

        return data
