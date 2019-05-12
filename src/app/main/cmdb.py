import time
from app.utils.mylog import My_log
from app.main.conf import conf_data

from app import db
from app.main.dbmodel.cmdb import t_conf_host


logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class cmdb(object):
    """docstring for cmdb"""

    def __init__(self):
        super(cmdb, self).__init__()

    def search_host_ip(self, ip):
        data = t_conf_host.query.filter_by(ip_v4=ip).first()
        if data is not None:
            return {"recode": 0, "redata": [data.to_json()]}
        else:
            return {"recode": 4, "redata": "host not found"}

    def show_host_all(self):
        data = t_conf_host.query.all()
        if data is not None:
            result = []
            for i in data:
                result.append(i.to_json())
            return {"recode": 0, "redata": result}
        else:
            return {"recode": 4, "redata": "not data"}

    def add_host(self, mess):
        work_log.info(str(mess))
        data = t_conf_host(
            ip_v4=mess.get("ip_v4"),
            ip_v6=mess.get("ip_v6"),
            ip_v4_m=mess.get("ip_v4_m"),
            name=mess.get("name"),
            operating_system=mess.get("operating_system"),
            hostname=mess.get("hostname"),
            cpu_number=mess.get("cpu_number"),
            memory_size=mess.get("memory_size"),
            sn=mess.get("sn"),
            address=mess.get("address"),
            belong_machineroom=mess.get("belong_machineroom"),
            rack=mess.get("rack"),
            manufacturer=mess.get("manufacturer"),
            dev_type=mess.get("type"),
            dev_category=mess.get("dev_category"),
            produce=mess.get("produce"),
            level=mess.get("level"),
            info=mess.get("info"),
        )
        try:
            db.session.add(data)
            db.session.commit()
            work_log.info("add host --- yes")
            return {"recode": 0, "redata": "ok"}
        except Exception as e:
            work_log.error("add host --- error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "error"}

    def del_host(self, hostid):
        data = t_conf_host.query.filter_by(id=hostid).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
            return {"recode": 0, "redata": "del yes"}
        else:
            return {"recode": 4, "redata": "host not found"}

    def update_host(self, mess):
        try:
            work_log.debug(str(mess))
            hostid = mess.get("id")
            data = t_conf_host.query.filter_by(id=hostid).first()
            if not data:
                work_log.info("host id is not found %d" % hostid)
                return {"recode": 4, "redata": "host not found"}

            work_log.debug(str(data))
            data.id = (mess.get("id"),)
            data.ip_v4 = (mess.get("ip_v4"),)
            data.ip_v6 = (mess.get("ip_v6"),)
            data.ip_v4_m = (mess.get("ip_v4_m"),)
            data.name = (mess.get("name"),)
            data.operating_system = (mess.get("operating_system"),)
            data.hostname = (mess.get("hostname"),)
            data.cpu_number = (mess.get("cpu_number"),)
            data.memory_size = (mess.get("memory_size"),)
            data.sn = (mess.get("sn"),)
            data.address = (mess.get("address"),)
            data.belong_machineroom = (mess.get("belong_machineroom"),)
            data.rack = (mess.get("rack"),)
            data.manufacturer = (mess.get("manufacturer"),)
            data.dev_type = (mess.get("dev_type"),)
            data.dev_category = (mess.get("dev_category"),)
            data.produce = (mess.get("produce"),)
            data.level = (mess.get("level"),)
            data.info = mess.get("info")

            db.session.commit()
            work_log.info("update host --- yes")
            return {"recode": 0, "redata": "ok"}
        except Exception as e:
            work_log.error("update host --- error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "error"}

    def run_task(self, mess):
        if mess.get("unit") == "host" and mess.get("task") == "add":
            return self.add_host(mess.get("body"))
        elif mess.get("unit") == "host" and mess.get("task") == "del":
            return self.del_host(mess.get("id"))
        elif mess.get("unit") == "host" and mess.get("task") == "update":
            return self.update_host(mess.get("body"))
        elif mess.get("unit") == "host" and mess.get("task") == "show":
            return self.search_host_ip(mess.get("ip"))
        elif mess.get("unit") == "host" and mess.get("task") == "showall":
            return self.show_host_all()
