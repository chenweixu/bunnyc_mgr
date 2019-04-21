from app.utils.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.conf import conf_data

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class HostTask(object):
    """docstring for HostTask"""

    def __init__(self, data):
        super(HostTask, self).__init__()
        self.data = data

    def run(self):
        dest_obj = self.data.get("task")
        unit = self.data.get("unit")
        cmd = self.data.get("cmd")
        ip = self.data.get("ip")
        if dest_obj == "remote" and unit:
            info = HostBaseCmd(ip)
            new_data = info.run_unit_task(unit)
            return new_data

        if dest_obj == "remote" and cmd:
            work_log.info(f"remote exec cmd, ip: {ip}, cmd: {cmd}")
            user = self.data.get("user")
            default_user = conf_data("user_info", "default_user")
            if user and user != default_user:
                return {"recode": 1, "redata": "user error"}
            info = HostBaseCmd(ip)
            new_data = info.run_cmd_task(cmd)
            return new_data
