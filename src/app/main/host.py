from app.main.util.mylog import My_log
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
        if self.data.get("task") == "remote" and self.data.get("unit"):
            ip = self.data.get("ip")
            info = HostBaseCmd(ip)
            new_data = info.runtask(task=self.data.get("unit"))
            return new_data

        if self.data.get("task") == "remote" and self.data.get("cmd"):
            cmd = self.data.get("cmd")
            ip = self.data.get("ip")
            user = self.data.get("user")
            work_log.info("ip: %s, cmd: %s" % (ip, cmd))

            default_user = conf_data("user_info", "default_user")
            if user and user != default_user:
                return {"recode": 1, "redata": "user error"}

            info = HostBaseCmd(ip)
            new_data = info.runtask(cmd=cmd)
            return new_data
