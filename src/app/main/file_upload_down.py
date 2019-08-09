import os
from app.utils.mylog import My_log
from app.main.server.hostbase import HostBaseCmd
from app.main.conf import conf_data
from app import work_log

class UpDownFile(HostBaseCmd):
    """docstring for UpDownFile"""

    def __init__(self, ip, user):
        HostBaseCmd.__init__(self, ip, user, scp=True)

    def upload(self, src, dest):
        work_log.info(f"upload: {src} -> {dest}")
        try:
            self.put(src, dest)
            return {"recode": 0, "redata": "上传成功"}
        except Exception as e:
            work_log.error("upload error")
            work_log.error(str(e))
            return {"recode": 9, "redata": "上传失败"}

    def down(self, src, localfile):
        work_log.info(f"down: {src}, {localfile}")
        try:
            self.get(src, localfile)
            return True
        except Exception as e:
            work_log.error("upload error")
            work_log.error(str(e))
            return False

class DownRemoteFile(object):
    """docstring for DownRemoteFile"""
    def __init__(self, data):
        super(DownRemoteFile, self).__init__()
        self.data = data

    def down(self):
        try:
            ip = self.data.get("ip")
            file = self.data.get("file")
            user = self.data.get("user")
            if self.data.get("task") != 'remote_file_down':
                return {"recode": 1, "redata": "req arg error"}

            work_log.info(f"down file, ip: {ip}, filename: {file}, user: {user}")

            tmp_dir = conf_data("work_tmp_dir")
            filename = os.path.basename(file)
            local_tmp = os.path.join(tmp_dir, filename)

            info = UpDownFile(ip, user)
            data = info.down(file, local_tmp)
            if data:
                return {"recode": 0, "redata": f"api/v2/downfile/{filename}"}
            else:
                return {"recode": 2, "redata": "file not fount"}

        except Exception as e:
            work_log.error("down file run error")
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}

# class UpLoadFile(object):
#     """docstring for UpLoadFile"""
#     def __init__(self, data):
#         super(UpLoadFile, self).__init__()

#     def upload(self):
#         pass
