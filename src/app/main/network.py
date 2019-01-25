from app.main.util.mylog import My_log
from app.main.network_manager import NetworkManager
from app.main.hostshell import HostBaseCmd
from app.main.conf import conf_data

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class NetWork(object):
    """docstring for NetWork"""
    def __init__(self):
        super(NetWork, self).__init__()

    def ping(self, ipaddr):
        info = NetworkManager()
        data = info.local_ping(ipaddr)
        work_log.info(str(data))
        return data

    def run_task(self, data):
        task = data.get("task")
        work_log.debug(str(data))
        if task == "check_port":
            source_ip = data.get("source")
            des_ip = data.get("ip")
            des_port = data.get("port")

            if source_ip == "localhost":
                info = NetworkManager()
                try:
                    redata = info.port_scan(des_ip, des_port)
                    if redata == 0:
                        recode = 0
                    else:
                        recode = 4
                except Exception as e:
                    work_log.error(str(e))
                    redata = "scan error"
                    recode = 2

                data = {"recode": recode, 'redata': redata}
                return data
            else:
                info = HostBaseCmd(source_ip, scp=True)
                redata = info.net_port_scan(ip=des_ip, port=des_port)
                if redata == 0:
                    recode = 0
                else:
                    recode = 4
                data = {"recode": recode, 'redata': redata}
                work_log.debug("port scan status: "+str(data))
                return data

        elif task == "iptable":
            return {"recode": 1, 'redata': "未开放"}
        else:
            work_log.debug(str("task not found"))
            return {"recode": 1, 'redata': "参数错误"}
