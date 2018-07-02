#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/12 14:05
# @Author  : hyang
# @File    : ps_shell.py
# @Software: PyCharm

import time
import os

from colorama import init, Fore,Style
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)  # 加入环境变量
from utils import cmd_utils
from utils import my_logset
from conf import shell_set
from conf import settings
from utils import time_utils


class PsCmd(object):
    """
    进程检查
    """
    def __init__(self, log_file=settings.psLogPath):
        self.shell_log = my_logset.get_mylogger("ps-shell")
        init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
        self.ps_dict = shell_set.ps_shell
        self.log_file = log_file.format(time_utils.get_curr_dt())
        self.f = open(self.log_file, 'a+', encoding='utf-8')

    def __del__(self):
        self.f.close()

    def ops_ps_cmd(self, ps_name='all', op_type='cat'):
        """
         操作进程
        :param ps_name:
        :param op_type:
        :return:
        """

        self.f.write('\n\n------------------{}操作进程开始--------------\n\n'.format(time_utils.get_curr_dt()+time_utils.get_curr_time()))
        if ps_name == 'all':
            for item in self.ps_dict:
                    self.__print_proc_info(self.ps_dict, item,op_type)

        else:
            if ps_name in self.ps_dict.keys():
                self.__print_proc_info(self.ps_dict, ps_name,op_type)
            else:
                print(Fore.RED+Style.BRIGHT+'进程{}不存在'.format(ps_name))
                self.f.write('进程{}不存在\n'.format(ps_name))
        print(Fore.GREEN + Style.BRIGHT + '日志文件' + self.log_file)
    def __print_proc_info(self, ps_dict, item, op_type):
        """
        print
        :param item:
        :return:
        """

        msg = '%s进程 %s' % (op_type,ps_dict.get(item).get('name'))
        print(Fore.YELLOW +Style.BRIGHT + msg)
        self.f.write('*'*30+"\n"+msg+"\n")
        ps_cmd = ps_dict.get(item).get('ps_cmd')
        ret = cmd_utils.cmd_exec(ps_cmd)
        cmd_utils.cmd_exec('sleep 2')
        if ret['code'] == 0:
            if ret['res']:
                if op_type == 'stop':
                    print(Fore.RED +Style.BRIGHT+ 'kill ' + ret['res'].strip())
                    self.f.write('kill ' + ret['res'].strip() + "\n")
                    # for item_ret in ret['res']:
                    kill_cmd = 'kill -9 %s' % ret['res'].strip()
                    k_ret = cmd_utils.cmd_exec(kill_cmd)
                    cmd_utils.cmd_exec('sleep 3 ')
                elif op_type == 'cat':
                    print(Fore.MAGENTA + Style.BRIGHT + '进程号:'+ret['res'].strip())
                    self.f.write('进程号' + ret['res'].strip() + "\n")
                else:
                    print(Fore.MAGENTA + Style.BRIGHT + '进程已启动，进程号:' + ret['res'].strip())
                    self.f.write('进程号' + ret['res'].strip() + "\n")
            else:
                if op_type == 'start':
                    cmd_path = ps_dict.get(item).get('path')
                    start_cmd = ps_dict.get(item).get('start_cmd')
                    cd_ret = cmd_utils.cmd_exec('cd %s' % cmd_path)
                    if cd_ret['code'] == 0:
                        log_path = ps_dict.get(item).get('run_log')
                        cmd_utils.cmd_exec('mv %s %s_%s' %(log_path, log_path,str(int(time.time()))))
                        os.chdir(cmd_path)  # 切换路径
                        start_ret = cmd_utils.cmd_exec(start_cmd)
                        cmd_utils.cmd_exec('sleep 10')
                        # print(start_ret)
                        log_ret = cmd_utils.cmd_exec('tail -30 {}'.format(log_path))
                        print(Fore.RED +Style.BRIGHT+ '-------------启动日志{}------------\n'.format(ps_dict.get(item).get('run_log')) + log_ret['res'] + "\n")

                        self.f.write('-------------启动日志{}------------\n'.format(ps_dict.get(item).get('run_log')) + log_ret['res'] + "\n")
                    else:
                        print(Fore.RED +Style.BRIGHT+ '进程[%s]所在路径[%s]不存在 '% (ps_dict.get(item).get('name'),cmd_path))
                        self.f.write('进程[%s]所在路径[%s]不存在\n '% (ps_dict.get(item).get('name'),cmd_path))

                else:
                    print(Fore.RED + Style.BRIGHT+'进程未启动')
                    self.f.write('进程未启动'+"\n")

if __name__ == '__main__':
    pass
    # import os
    # import sys
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(BASE_DIR)  # 加入环境变量
    s = PsCmd()
    s.ops_ps_cmd('all')
    # s.ops_ps_cmd('stop')
    # s.ops_ps_cmd('start')
