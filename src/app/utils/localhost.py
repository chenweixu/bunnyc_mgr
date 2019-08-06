import os
import re
import subprocess
from app import work_log


class local_task_exec(object):
    """docstring for local_task_exec"""

    def __init__(self):
        super(local_task_exec, self).__init__()

    def cmd(self, cmd_body):
        work_log.info(str(cmd_body))
        sub = subprocess.run(cmd_body, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode,out,err=sub.returncode,sub.stdout,sub.stderr
        if returncode:
            return err.decode()
        else:
            return out.decode().splitlines()

    def unit(self, name):
        if name == "disk":
            return self.cmd('df')
        if name == "diskinfo":
            return self._get_disk_info()
        elif name == "uptime":
            return self.cmd('uptime')
        elif name == "uptime_dict":
            return self._uptime_dict()
        elif name == "cpu":
            return self.cmd('sar 1 3')
        elif name == "meminfo":
            return self._hw_mem_proc()
        else:
            return "name error"

    def run_script(self, file):
        body = 'bash '+ file
        return self.cmd(body)


    def _uptime_dict(self):
        uptime = self.cmd('uptime')[0]
        info = uptime.split()
        data = {
            "curr_time": info[0],
            "run_time": info[2],
            "user_sum": info[3],
            "ld_1": info[7],
            "ld_5": info[8],
            "ld_15": info[9],
        }
        return data

    def _hw_mem_proc(self):
        data = open("/proc/meminfo", "r").readlines()
        meminfo = {}
        for i in data:
            key = re.findall(r".*:", i)[0].strip(":")
            val = int(re.findall(r"\b[0-9]+", i)[0])
            meminfo[key] = val
        return meminfo

    def _get_disk_info(self):
        disk = self.cmd('df')
        data = {}
        for i in disk[1:]:
            p_info = i.split()
            p_data = {
                "p_dev_name": p_info[0],
                "p_sum": p_info[1],
                "p_used": p_info[2],
                "p_free": p_info[3],
                "p_used_rate": p_info[4],
                "p_name": p_info[5],
            }
            data[p_info[5]] = p_data
        return data


# class Get_Host_data(object):
#     """docstring for Get_Host_data"""

#     def __init__(self, ip, type):
#         super(Get_Host_data, self).__init__()
#         self.ip = ip
#         self.type = type

#     def get_meminfo(self):
#         # 将 meminfo 文件内容转为一个字典
#         data = open("/proc/meminfo", "r").readlines()
#         meminfo = {}
#         for i in data:
#             key = re.findall(r".*:", i)[0].strip(":")
#             val = int(re.findall(r"\b[0-9]+", i)[0])
#             meminfo[key] = val
#         meminfo["host_ip"] = self.ip
#         meminfo["type"] = self.type
#         return meminfo

