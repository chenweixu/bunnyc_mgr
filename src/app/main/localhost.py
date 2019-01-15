import os
import re
import subprocess


class Local_hosts_info(object):
    """docstring for Local_hosts_info"""

    def __init__(self):
        super(Local_hosts_info, self).__init__()

    def hw_df(self):
        cmd = subprocess.Popen(["df"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = cmd.communicate()
        return out.decode().splitlines()

    def hw_uptime(self):
        cmd = subprocess.Popen(
            ["uptime"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, error = cmd.communicate()
        return out.decode().splitlines()

    def uptime_dict(self):
        uptime = self.hw_uptime()[0]
        info = bytes.decode(uptime).split()
        data = {
            "curr_time": info[0],
            "run_time": info[2],
            "user_sum": info[3],
            "ld_1": info[7],
            "ld_5": info[8],
            "ld_15": info[9],
        }
        return data

    def hw_cpu(self):
        cmd = subprocess.Popen(
            ["sar", "1", "3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, error = cmd.communicate()
        cpu = out.decode().splitlines()
        return cpu

    def hw_mem_proc(self):
        data = open("/proc/meminfo", "r").readlines()
        meminfo = {}
        for i in data:
            key = re.findall(r".*:", i)[0].strip(":")
            val = int(re.findall(r"\b[0-9]+", i)[0])
            meminfo[key] = val
        txt = meminfo.items()
        return txt

    def get_disk_info(self):
        cmd = subprocess.Popen(["df"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = cmd.communicate()
        disk = out.splitlines()
        data = {}
        for i in disk[1:]:
            p_info = bytes.decode(i).split()
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

    def get_local_dir_file(self):
        local_dir = os.getcwd()
        cmd = "ls %s" % local_dir
        files = os.popen(cmd).read()
        return files

    def hwinfo(self, task):
        if task == "disk":
            txt = self.hw_df()
        elif task == "uptime":
            txt = self.hw_uptime()
        elif task == "cpu":
            txt = self.hw_cpu()
        elif task == "meminfo":
            txt = self.hw_mem_proc()
        else:
            txt = "task error"
        return txt


class Get_Host_data(object):
    """docstring for Get_Host_data"""

    def __init__(self, ip, type):
        super(Get_Host_data, self).__init__()
        self.ip = ip
        self.type = type

    def get_meminfo(self):
        # 将 meminfo 文件内容转为一个字典
        data = open("/proc/meminfo", "r").readlines()
        meminfo = {}
        for i in data:
            key = re.findall(r".*:", i)[0].strip(":")
            val = int(re.findall(r"\b[0-9]+", i)[0])
            meminfo[key] = val
        meminfo["host_ip"] = self.ip
        meminfo["type"] = self.type
        return meminfo

