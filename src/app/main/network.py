from app.main.network_manager import NetworkManager
from app.main.server.hostbase import HostBaseCmd
from app.main.conf import conf_data
from app import work_log


class NetWork(object):
    """docstring for NetWork"""
    def __init__(self):
        super(NetWork, self).__init__()

    def ping(self, ipaddr):
        info = NetworkManager()
        data = info.local_ping(ipaddr)
        work_log.info(str(data))
        return data

    def local_check_port(self, ip, port):
        work_log.debug('local exec remote port test')
        info = NetworkManager()
        try:
            recode = info.port_scan(ip, port)
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

    def remote_check_port(self, server, ip, port):
        work_log.info('login remote server check port')
        try:
            info = HostBaseCmd(server, scp=True)
            redata = info.net_port_scan(ip=ip, port=port)
        except Exception as e:
            work_log.error(str(e))
            return {"recode": 9, 'redata': '连接服务器失败'}

        work_log.debug("port scan status: "+str(redata))
        if redata == 0:
            return {"recode": 0, 'redata': '探测成功'}
        else:
            return {"recode": 4, 'redata': '探测失败'}

    def check_port(self, data):
        source = data.get("source")
        des_ip = data.get("ip")
        des_port = data.get("port")

        if not source or source == 'localhost':
            return self.local_check_port(des_ip, des_port)

        if source:
            return self.remote_check_port(source, des_ip, des_port)

        return {"recode": 1, 'redata': "参数错误"}

    def run_task(self, data):
        task = data.get("task")
        work_log.debug(str(data))
        if task == "check_port":
            return self.check_port(data)
        elif task == "iptable":
            return {"recode": 1, 'redata': "未开放"}
        else:
            work_log.debug(str("task not found"))
            return {"recode": 1, 'redata': "参数错误"}
