from app.utils.ssh import Myssh
from app.main.conf import conf_data
from app import work_log

class HostBaseCmd(Myssh):
    """docstring for HostBaseCmd
    单主机远程任务
    """

    def __init__(self, ip, user=None, scp=None):
        if not user:
            ssh_user = conf_data("user_info", "default_user")
        else:
            ssh_user = user
        try:
            ssh_pw = conf_data("user_info", str(ssh_user), "ssh_passwd")
            key = conf_data("user_info", str(ssh_user), "ssh_key")
            ssh_port = conf_data("user_info", "ssh_port")
        except Exception as e:
            work_log.info("ssh arg input error")
            work_log.info(str(e))
            raise e

        self.ip = ip

        if key:
            ssh_key = conf_data("work_conf_dir") + "/" + key

        try:
            if ssh_key and not scp:
                Myssh.__init__(self, ip, ssh_user, keys=ssh_key, port=ssh_port)
            elif ssh_key and scp:
                Myssh.__init__(self, ip, ssh_user, keys=ssh_key, port=ssh_port, scp=True)
            elif ssh_pw and scp:
                Myssh.__init__(self, ip, ssh_user, passwd=ssh_pw, port=ssh_port, scp=True)
            elif ssh_pw and not scp:
                Myssh.__init__(self, ip, ssh_user, passwd=ssh_pw, port=ssh_port)

        except Exception as e:
            work_log.error('ssh login server error')
            work_log.error(str(e))
            raise e


    def ssh_cmd(self, cmd, stdout=False):
        work_log.info("ssh_cmd host: %s cmd: %s" % (self.ip, cmd))
        try:
            run_stdout, run_stderr = self.runshell(cmd)

            if run_stderr:
                # 先记录执行的错误输出
                work_log.error("ssh_cmd is error stdout")
                work_log.error(str(run_stderr))

            # 需要标准输出的情况
            if stdout:
                if run_stderr:
                    return [2, run_stderr.decode("utf-8")]
                else:
                    work_log.debug("ssh_cmd success, run_stdout")
                    work_log.debug(str(run_stdout))
                    return [0, run_stdout.decode("utf-8")]

            # 不需要标准输出的情况
            if run_stderr:
                return [2, run_stderr.decode("utf-8")]
            else:
                work_log.debug("ssh_cmd success, run_stdout")
                work_log.debug(str(run_stdout))
                return [0, "success"]
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

    def run_unit_task(self, arg):

        if arg in conf_data('shell_unit'):
            cmd = conf_data('shell_unit', arg)
        else:
            return {"recode": 9, "redata": 'unit error'}

        try:
            recode, data = self.ssh_cmd(cmd, stdout=True)
            return {"recode": recode, "redata": data}
        except Exception as e:
            work_log.error("run_unit_task error")
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}

    def run_cmd_task(self, cmd):
        try:
            recode, data = self.ssh_cmd(cmd, stdout=True)
            return {"recode": recode, "redata": data}
        except Exception as e:
            work_log.error("run_cmd_task error")
            work_log.error(str(e))
            return {"recode": 9, "redata": str(e)}

    def net_port_scan(self, ip, port):
        try:
            work_dir = conf_data("work_dir")
            source_file = work_dir + "/utils/port_scan.py"
            des_file = "/tmp/port_scan.py"
            work_log.debug("copy file to remote")
            self.ssh_file_put(source_file, des_file)
        except Exception as e:
            work_log.error('scp port check file to remote server error')
            return 9

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
        return recode
        work_log.debug("port scan recode: %s" % recode)

