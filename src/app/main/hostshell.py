from app.main.ssh import Myssh
from app.main.conf import conf_data
from app.main.mylog import My_log
from multiprocessing import Pool

logfile = conf_data("work_log")
log_evel = conf_data("log_level")
work_log = My_log(logfile, log_evel).get_log()


class HostBaseCmd(Myssh):
    """docstring for HostBaseCmd"""

    def __init__(self, ip, user=None, scp=None):
        userinfo = conf_data("user_info")
        if not user:
            ssh_user = conf_data("user_info", "default_user")
        else:
            ssh_user = user

        ssh_pw = conf_data("user_info", ssh_user, "ssh_passwd")
        key = conf_data("user_info", ssh_user, "ssh_key")
        ssh_port = conf_data("user_info", "ssh_port")
        self.ip = ip

        if key:
            ssh_key = conf_data("work_dir") + "/conf/" + key

        if ssh_key and not scp:
            Myssh.__init__(self, ip, ssh_user, keys=ssh_key, port=ssh_port)

        elif ssh_key and scp:
            Myssh.__init__(self, ip, ssh_user, keys=ssh_key, port=ssh_port, scp=True)

        elif ssh_pw and scp:
            Myssh.__init__(self, ip, ssh_user, passwd=ssh_pw, port=ssh_port, scp=True)

        elif ssh_pw and not scp:
            Myssh.__init__(self, ip, ssh_user, passwd=ssh_pw, port=ssh_port)

    def ssh_cmd(self, cmd, stdout=False):
        work_log.info("ssh_cmd host: %s cmd: %s" % (self.ip, cmd))
        try:
            run_stdout, run_stderr = self.runshell(cmd)

            if stdout:
                if run_stderr:
                    work_log.error("ssh_cmd error, run_stderr")
                    work_log.error(str(run_stderr))
                    return [1, run_stderr.decode("utf-8")]
                else:
                    work_log.debug("ssh_cmd success, run_stdout")
                    work_log.debug(str(run_stdout))
                    return [0, run_stdout.decode("utf-8")]

            if run_stderr:
                work_log.error("ssh_cmd error, run_stderr")
                work_log.error(str(run_stderr))
                return 1
            else:
                work_log.debug("ssh_cmd success, run_stdout")
                work_log.debug(str(run_stdout))
                return 0
        except Exception as e:
            work_log.error("ssh_cmd Exception error")
            work_log.error(str(e))
            return False

    def ssh_file_put(self, source_file, des_file):
        work_log.info("ssh_file_put host: %s =>> %s" % (source_file, des_file))
        try:
            self.put(source_file, des_file)
            work_log.info("ssh_file_put success")
        except Exception as e:
            work_log.error("ssh_file_put error")
            work_log.error(str(e))
            return False

    def runtask(self, cmd=None, task=None):
        if task and not cmd:
            if task == "disk":
                cmd = "df -h"
            if task == "mem":
                cmd = "free -g"
            if task == "netlistening":
                cmd = "netstat -tnlp"
            if task == "netss":
                cmd = "/usr/sbin/ss -s"
            if task == "uptime":
                cmd = "uptime"
            if task == "netrxtx":
                cmd = "sar -n DEV 1 3"
            if task == "vmstat":
                cmd = "vmstat 1 5 -t -S M"
            if task == "cpu":
                cmd = "sar -u 1 3"
        recode, data = self.ssh_cmd(cmd, stdout=True)

        newdata = {"ip": self.ip, "data": data, "recode": recode}
        return newdata

    def net_port_scan(self, ip, port):
        try:
            work_dir = conf_data("work_dir")
            source_file = work_dir + "/main/port_scan.py"
            des_file = "/tmp/port_scan.py"
            work_log.debug("copy file to remote")
            self.ssh_file_put(source_file, des_file)
        except Exception as e:
            raise e

        cmd0 = "chmod u+x " + des_file
        cmd1 = des_file + " " + ip + " " + str(port)
        cmd2 = "rm " + des_file

        try:
            work_log.debug("chmod file")
            self.ssh_cmd(cmd0)

            work_log.debug("exec remote file")
            cmdstatus, taskstatus = self.ssh_cmd(cmd1, stdout=True)
            work_log.info(str(taskstatus))

            work_log.debug("rm file to remote")
            self.ssh_cmd(cmd2)

            recode = int(taskstatus.rstrip("\n"))
            work_log.info(str(recode))
        except Exception as e:
            work_log.error("remote exec cmd error")
            work_log.error(str(e))
            recode = 2

        new_data = {"recode": recode}

        work_log.debug(str(new_data))
        return new_data


class HostGroupCmd(object):
    """docstring for HostGroupCmd"""

    def __init__(self, user, hostlist):
        super(HostGroupCmd, self).__init__()
        self.user = user
        self.hostlist = hostlist

    def _ssh_cmd(self, host, cmd):
        ssh = HostBaseCmd(host, self.user)
        stdout = ssh.ssh_cmd(cmd)
        return stdout

    def run(self, cmd, processes=8):
        pool = Pool(processes=processes)
        info = []
        for host in self.hostlist:
            info.append(pool.apply_async(self._ssh_cmd, (host, cmd)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data
