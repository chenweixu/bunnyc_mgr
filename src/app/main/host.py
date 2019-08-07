from app.main.server.hostbase import HostBaseCmd
from app.main.server.hostgroup import HostGroupCmd
from app.main.conf import conf_data
from app import work_log


class HostTask(object):
    """docstring for HostTask"""

    def __init__(self, data):
        super(HostTask, self).__init__()
        self.data = data

    def run(self):
        task = self.data.get("task")
        arg = self.data.get("arg")
        ip = self.data.get("ip")
        user = self.data.get("user")
        work_log.info(str(self.data))

        if not user:
            user = conf_data("user_info", "default_user")
        elif user not in conf_data("user_info"):
            return {"recode": 1, "redata": "input user error"}

        if task == 'shell':
            try:
                info = HostBaseCmd(ip, user=user)
                return info.run_cmd_task(arg)
            except AttributeError as e:
                work_log.error("ssh session create error")
                work_log.error(str(e))
                return {"recode": 1, "redata": "input format error"}
            except Exception as e:
                work_log.error("run_cmd_task error")
                work_log.error(str(e))
                return {"recode": 9, "redata": "run other error"}

        elif task == 'unit':
            info = HostBaseCmd(ip, user=user)
            return info.run_unit_task(arg)
        elif task == 'script':
            info = HostBaseCmd(ip, user=user)
            return info.run_cmd_task(arg)
        else:
            work_log.info("req format error")
            return {"recode": 1, "redata": "format error"}


class HostsTask(object):
    """docstring for HostsTask"""

    def __init__(self, data):
        super(HostsTask, self).__init__()
        self.data = data

    def run(self):
        work_log.info(str(self.data))
        task = self.data.get("task")
        arg = self.data.get("arg")
        ip = self.data.get("ip")
        user = self.data.get("user")
        group = self.data.get("group")

        if group in conf_data('host_mgr_type'):
            ip = conf_data('host_mgr_type', group)
        else:
            work_log.info("group name error")
            return {"recode": 1, "redata": "format error"}

        if not user:
            user = conf_data("user_info", "default_user")
        elif user not in conf_data("user_info"):
            return {"recode": 1, "redata": "input user error"}

        if task == 'shell':
            try:
                info = HostGroupCmd(ip, user=user)
                return info.run_cmd_task(arg)
            except AttributeError as e:
                work_log.error("ssh session create error")
                work_log.error(str(e))
                return {"recode": 1, "redata": "input format error"}
            except Exception as e:
                work_log.error("run_cmd_task error")
                work_log.error(str(e))
                return {"recode": 9, "redata": "run other error"}

        elif task == 'unit':
            info = HostGroupCmd(ip, user=user)
            return info.run_unit_task(arg)
        elif task == 'script':
            info = HostGroupCmd(ip, user=user)
            return info.run_cmd_task(arg)
        else:
            work_log.info("req format error")
            return {"recode": 1, "redata": "format error"}


