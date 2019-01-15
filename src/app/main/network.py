from app.main.mylog import My_log
from app.main.networkmanager import NetworkManager
from app.main.hostshell import HostBaseCmd

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class Network(object):
    """docstring for Network"""
    def __init__(self):
        super(Network, self).__init__()

    def ping(ipaddr):
        info = NetworkManager()
        data = info.local_ping(ipaddr)
        work_log.info(str(data))
        return data

    def run_task(data):
        task = data.get("task")
        work_log.debug(str(data))
        if task == "check_port":
            source_ip = data.get("sip")
            des_ip = data.get("ip")
            des_port = data.get("port")

            if source_ip == "127.0.0.1":
                info = NetworkManager()
                try:
                    recode = info.port_scan(des_ip, des_port)
                except Exception as e:
                    work_log.error(str(e))
                    recode = "1"
                data = {"recode": recode, 'redata': ''}
                return data
            else:
                info = HostBaseCmd(source_ip, scp=True)
                data = info.net_port_scan(ip=des_ip, port=des_port)
                work_log.debug(str(data))
                data['redata'] = ''
                return data

        elif task == "iptable":
            return "", 404
        else:
            work_log.debug(str("task not found"))
            return "", 404
