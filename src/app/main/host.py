from app.main.mylog import My_log
from app.main.hostshell import HostBaseCmd

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()

class HostTaskInfo(object):
    """docstring for HostTaskInfo"""
    def __init__(self, data):
        super(HostTaskInfo, self).__init__()
        self.data = data

    def run():
        des_ip = self.data.get("des_ip")
        task = self.data.get("task")

        info = HostBaseCmd(des_ip)
        new_data = info.runtask(task=task)
        return new_data

        if task == 'cmd':
            user = self.data.get("user")
            work_log.info("user: %s, des_ip: %s, cmd: %s" % (user, des_ip, cmd))

            default_user = conf_data('user_info','default_user')
            if user != default_user:
                new_data = {'recode': 2, 'redata': 'user error'}
                return new_data

            info = HostBaseCmd(des_ip)
            new_data = info.runtask(cmd=cmd)
            return new_data
