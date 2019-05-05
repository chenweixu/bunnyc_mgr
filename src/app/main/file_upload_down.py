import os
from app.utils.mylog import My_log
from app.main.hostshell import HostBaseCmd
from app.main.conf import conf_data

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()

class UpDownFile(HostBaseCmd):
    """docstring for UpDownFile"""

    def __init__(self, ip, user):
        HostBaseCmd.__init__(self, ip, user, scp=True)

    def upload(self, src, dest):
        work_log.info(f'upload: {src} -> {dest} ')
        try:
            self.put(src, dest)
            return { "recode": 0, "redata": '上传成功'}
        except Exception as e:
            work_log.error('upload error')
            work_log.error(str(e))
            return { "recode": 9, "redata": '上传失败'}

    def down(self, src, localfile):
        work_log.info(f'down: {src}, {localfile}')
        try:
            self.get(src, localfile)
            return True
        except Exception as e:
            work_log.error('upload error')
            work_log.error(str(e))
            return False



# class UpDownFile(object):
#     """docstring for UpDownFile"""

#     def __init__(self, ip, user):
#         super(UpDownFile, self).__init__()
#         self.ip = ip
#         self.user = user

#     def upload(self, src, dest):
#         work_log.info(f'upload: {src} -> {dest} ')
#         session = HostBaseCmd(self.ip, self.user, scp=True)
#         session.ssh_file_put(src, dest)

#     def down(self, src):
#         pass
