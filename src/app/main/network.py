from app.utils.mylog import My_log
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
            source_ip = data.get("sip")
            des_ip = data.get("ip")
            des_port = data.get("port")

            if not source_ip:
                work_log.debug('local exec remote port test')
                info = NetworkManager()
                try:
                    recode = info.port_scan(des_ip, des_port)
                    if recode == 0:
                        return {"recode": recode, 'redata': '成功'}
                    elif recode == 1:
                        return {"recode": 4, 'redata': '主机存在端口不可访问'}
                    else:
                        return {"recode": 4, 'redata': '目标不能访问'}
                except Exception as e:
                    work_log.error(str(e))
                    redata = "scan error"
                    return {"recode": 2, 'redata': '程序错误'}
            if source_ip:
                info = HostBaseCmd(source_ip, scp=True)
                redata = info.net_port_scan(ip=des_ip, port=des_port)
                work_log.debug("port scan status: "+str(redata))
                if redata == 0:
                    return {"recode": 0, 'redata': '探测成功'}
                else:
                    return {"recode": 4, 'redata': '探测失败'}

        elif task == "iptable":
            return {"recode": 1, 'redata': "未开放"}
        else:
            work_log.debug(str("task not found"))
            return {"recode": 1, 'redata': "参数错误"}
