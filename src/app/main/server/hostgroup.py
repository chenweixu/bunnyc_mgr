from app import work_log
from app.main.server.hostbase import HostBaseCmd
from app.main.conf import conf_data
from multiprocessing import Pool

class HostGroupCmd(object):
    """docstring for HostGroupCmd
    多主机远程任务
    """

    def __init__(self, hostlist, user, processes=8):
        super(HostGroupCmd, self).__init__()
        # if len(hostlist) == 1:
        #     hostlist = 'xxx'

        self.hostlist = hostlist
        self.user = user
        self.processes = processes

    def _ssh_cmd(self, host, cmd, stdout=False):
        try:
            ssh = HostBaseCmd(host, self.user)
            data = ssh.ssh_cmd(cmd, stdout=stdout)
            return data
        except Exception as e:
            work_log.error(str(e))
            return [2, str(e)]


    def run_cmd_task(self, arg, stdout=False):
        pool = Pool(processes=self.processes)
        info = []
        for host in self.hostlist:
            info.append(pool.apply_async(self._ssh_cmd, (host, arg, stdout)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        work_log.info(str(data))
        return data


    def run_unit_task(self, arg, stdout=False):
        if arg in conf_data('shell_unit'):
            cmd = conf_data('shell_unit', arg)
            data = self.run_cmd_task(cmd, stdout)
            return data
        else:
            return {"recode": 9, "redata": 'unit error'}
        # try:
        #     recode, data = self.run_cmd_task(cmd)
        #     return {"recode": recode, "redata": data}
        # except Exception as e:
        #     work_log.error("run_unit_task error")
        #     work_log.error(str(e))
        #     return {"recode": 9, "redata": str(e)}



    def run(self, cmd, processes=8):
        pool = Pool(processes=processes)
        info = []
        work_log.debug(str(self.hostlist))
        for host in self.hostlist:
            info.append(pool.apply_async(self._ssh_cmd, (host, cmd)))
        pool.close()
        pool.join()

        data = []
        for i in info:
            data.append(i.get())
        return data
