import time
from sqlalchemy import func
from app import db
from app import work_log
from app.main.dbmodel.logdb import t_host_cpu

class MonitorTask(object):
    """docstring for MonitorTask"""

    def __init__(self):
        super(MonitorTask, self).__init__()

    def HostUptimeData(self, data):
        ip = data.get("ip")
        # current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        old_time = time.strftime("%Y-%m-%d_%X", time.localtime(time.time() - 3600))

        try:
            abc = (
                db.session.query(
                    func.date_format(t_host_cpu.ctime, "%H:%i:%s").label("ctime"),
                    t_host_cpu.ld_1,
                    t_host_cpu.ld_2,
                    t_host_cpu.ld_3,
                )
                .filter(t_host_cpu.ip == ip, t_host_cpu.ctime > old_time)
                .all()
            )
        except Exception as e:
            work_log.error('select db HostUptimeData error')
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}

        x_name = []
        ld_1 = []
        ld_5 = []
        ld_15 = []

        for i in abc:
            x_name.append(str(i.ctime))
            ld_1.append(format(i.ld_1, ".2f"))
            ld_5.append(format(i.ld_2, ".2f"))
            ld_15.append(format(i.ld_3, ".2f"))

        value = {
            "x_name": x_name,
            "y_data": {"ld_1": ld_1, "ld_5": ld_5, "ld_15": ld_15},
        }

        return {"recode": 0, "redata": value}

    def HostCpuData(self, data):
        ip = data.get("ip")
        # current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        old_time = time.strftime("%Y-%m-%d_%X", time.localtime(time.time() - 3600))

        try:
            abc = (
                db.session.query(
                    func.date_format(t_host_cpu.ctime, "%H:%i:%s").label("ctime"),
                    t_host_cpu.cpu,
                )
                .filter(t_host_cpu.ip == ip, t_host_cpu.ctime > old_time)
                .all()
            )
        except Exception as e:
            work_log.error('select db HostCpuData error')
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}

        x_name = []
        cpu = []
        work_log.debug(str(abc))
        for i in abc:
            x_name.append(str(i.ctime))
            cpu.append(format(i.cpu, ".2f"))

        value = {"x_name": x_name, "y_data": {"cpu": cpu}}

        return {"recode": 0, "redata": value}

    def run(self, data):
        types = data.get("types")
        unit = data.get("unit")
        if not types == "host":
            return {"recode": 1, "redata": "format error"}
        if unit == "uptime":
            return self.HostUptimeData(data)
        if unit == "cpu":
            return self.HostCpuData(data)


        return {"recode": 1, "redata": "format error"}
