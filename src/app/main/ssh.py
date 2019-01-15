#!/usr/bin/python
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2016-12-27 23:15:32
__author__ = "chenwx"

import paramiko


class Myssh(object):
    """docstring for Myssh
    执行一条命令 | 上传和下载文件/目录
    """

    def __init__(
        self,
        ip,
        user,
        passwd=None,
        keys=None,
        pkey_type="rsa",
        port=22,
        timeout=5,
        scp=None,
    ):
        super(Myssh, self).__init__()

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if keys:
            if pkey_type == "rsa":
                mykey = paramiko.RSAKey.from_private_key_file(keys)
            elif pkey_type == "dsa":
                mykey = paramiko.DSSKey.from_private_key_file(keys)
            else:
                raise Exception("keys type not rsa dsa")

            self.ssh.connect(ip, int(port), username=user, pkey=mykey, timeout=timeout)

            if scp:
                t = self.ssh.get_transport()
                self.sftp = paramiko.SFTPClient.from_transport(t)
        else:
            self.ssh.connect(
                ip, int(port), username=user, password=passwd, timeout=timeout
            )

            if scp:
                t = self.ssh.get_transport()
                self.sftp = paramiko.SFTPClient.from_transport(t)

    def __del__(self):
        if hasattr(self, "sftp"):
            self.sftp.close()
        if hasattr(self, "ssh"):
            self.ssh.close()

    def runshell(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        run_stdout = stdout.read()
        run_stderr = stderr.read()
        return run_stdout, run_stderr

    def get(self, remote_file, local_file):
        self.sftp.get(remote_file, local_file)

    def put(self, local_file, remote_file):
        self.sftp.put(local_file, remote_file)

    def get_dirs(self, remote_dir, local_dir):
        self.sftp.get(remote_dir, local_dir)

    def put_dirs(self, remote_dir, local_dir):
        self.sftp.put(local_dir, remote_dir)
