from flask import request
from app import work_log
from app.utils.localhost import local_task_exec

class LocalTask(object):
    """docstring for LocalTask"""

    def __init__(self, data):
        super(LocalTask, self).__init__()
        self.data = data
        self.task = local_task_exec()

    def cmd(self, cmd_body):
        work_log.info('cmd')
        redata = self.task.cmd(cmd_body)
        data = {"recode": 0, "redata": redata}
        return data

    def unit(self, name):
        work_log.info('unit')
        redata = self.task.unit(name)
        data = {"recode": 0, "redata": redata}
        return data

    def script(self, file):
        work_log.info('script')
        redata = self.task.run_script(file)
        data = {"recode": 0, "redata": redata}
        return data

    def file_upload(self):
        work_log.info('file_upload')
        data = {"recode": 0, "redata": 'yes'}
        return data

    def file_down(self):
        work_log.info('file_down')
        data = {"recode": 0, "redata": 'yes'}
        return data

    def run(self):
        work_log.debug(str(self.data))
        task = self.data.get("task")
        unit = self.data.get("unit")
        file = self.data.get("file")
        if task == 'cmd':
            cmd = self.data.get("cmd")
            return self.cmd(cmd)
        elif task == 'unit':
            return self.unit(unit)
        elif task == 'script':
            return self.script(file)
        elif task == 'file_upload':
            return self.file_upload()
        elif task == 'file_down':
            return self.file_down()
        else:
            work_log.error('form error')
            return {"recode": 1, "redata": "format error"}
