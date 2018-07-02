#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 11:01
# @Author  : hyang
# @File    : shell_cmd.py
# @Software: PyCharm

import os

from utils import ssh_utils
from colorama import Fore
from utils import cmd_utils
from utils import my_logset

class ShellCmd(object):
    """
    shell脚本类
    """
    def __init__(self,run_name,run_path,run_cmd,run_log,run_host='localhost'):
        self.shell_log = my_logset.get_mylogger("shell")
        self.run_name = run_name  # shell 功能名
        self.run_cmd = run_cmd    # shell 脚本文件名
        self.run_log = run_log    # shell启动脚本日志
        self.run_path = run_path  # shell存放的路径
        self.run_host = run_host  # shell所在的host

    def start_lshell(self):
        """
        启动本地的shell
        :return:
        """
        self.shell_log.debug('shell run shell_func %s shell_name %s '% self.run_name,self.run_cmd)

        run_res = cmd_utils.cmd_exec(os.path.join(self.run_path,self.run_cmd))

        return run_res

    def stop_lshell(self):
        """
        停止本地的shell
        :return:
        """
        self.shell_log.debug('shell stop shell_func %s shell_name %s ' % self.run_name, self.run_cmd)

        run_res = cmd_utils.cmd_exec(os.path.join(self.run_path, self.run_cmd))
        print(run_res)
        if run_res:
            self.shell_log.info('run shell 进程号--', run_res)
            for item in run_res:
                self.shell_log.info('run shell 进程号--', run_res)
                ret = cmd_utils.cmd_exec('kill -9 %s' % item)
                cmd_utils.cmd_exec('sleep 5')
        else:
            self.shell_log.info('run shell [%s]进程不存在' % self.run_cmd )


    def start_rshell(self):
        """
        启动远程的shell
        :return
        """
        pass

    def stop_rshell(self):
        """
        停止远程的shell
        :return
        """