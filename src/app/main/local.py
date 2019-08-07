from flask import request
from app import work_log
from app.main.conf import conf_data
from app.utils.localhost import local_task_exec

class LocalTask(object):
    """docstring for LocalTask"""

    def __init__(self, data):
        super(LocalTask, self).__init__()
        self.data = data
        self.task = local_task_exec()

    def cmd(self, body):
        work_log.info(f'cmd: {body}')
        redata = self.task.cmd(body)
        data = {"recode": 0, "redata": redata}
        return data

    def unit(self, arg):
        work_log.info(f'unit: {arg}')
        if arg in conf_data('shell_unit'):
            cmd = conf_data('shell_unit', arg)
            redata = self.task.cmd(cmd)
        elif arg in ['disk_dict', 'uptime_dict', 'mem_dict']
            redata = self.task.unit(cmd)
        else:
            return {"recode": 9, "redata": 'unit error'}

        data = {"recode": 0, "redata": redata}
        return data

    def script(self, file):
        work_log.info(f'script: {file}')
        redata = self.task.run_script(file)
        data = {"recode": 0, "redata": redata}
        return data

    def run(self):
        work_log.debug(str(self.data))
        task = self.data.get("task")
        arg = self.data.get("arg")
        if task == 'cmd':
            return self.cmd(arg)
        elif task == 'unit':
            return self.unit(arg)
        elif task == 'script':
            return self.script(arg)
        else:
            work_log.error('form error')
            return {"recode": 1, "redata": "format error"}
