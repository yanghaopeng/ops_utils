#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 15:23
# @Author  : hyang
# @File    : disk_shell.py
# @Software: PyCharm


import re
# import os
# import sys
import csv
from prettytable import from_csv
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)  # 加入环境变量
from utils import cmd_utils
from utils import my_logset
from conf import shell_set
from conf import settings
from utils import time_utils


class DiskCmd(object):
    """
    磁盘检查
    """
    def __init__(self, log_file=settings.diskLogPath):
        self.shell_log = my_logset.get_mylogger("disk-shell")
        self.log_file = log_file.format(time_utils.get_curr_dt())
        self.f = open(self.log_file, 'w+', newline='',encoding='utf-8' )

    def __del__(self):
        self.f.close()

    def ops_disk_cmd(self, type='all'):
        """
        运行磁盘检查
        :return:
        """
        fieldnames = ['Dir', 'Use%', 'Avail','Used', 'Size']
        writer = csv.writer(self.f)
        writer.writerow(fieldnames)
        if type == 'half':
            df_ret = cmd_utils.cmd_exec(shell_set.df_half_shell)
        else:
            df_ret = cmd_utils.cmd_exec(shell_set.df_all_shell)
        if df_ret['code'] == 0:
            if df_ret['res']:
                  for item in df_ret['res'].split('\n')[:-1]:
                      d = re.split(r'\s+',item)
                      writer.writerow(d[-1:-6:-1])
            self.f.flush()  # 写入到磁盘

            self.f.seek(0)  # 把文件指针置于开头
            tb = from_csv(self.f)
            ### 设定左对齐
            tb.align = 'l'
            ### 设定T_ID右对齐
            tb.align["Use%"] = "r"
            ### 设定数字输出格式
            tb.float_format = "2.2"
            ### 设定边框连接符为'*"
            tb.junction_char = "*"
            # ### 设定排序列
            # tb.sortby = "Use%"
            # ### 设定排序方式
            # tb.reversesort = True
            ### 设定左侧不填充空白字符
            tb.left_padding_width = 0
            print(tb)

if __name__ == '__main__':
   d = DiskCmd()
   d.ops_disk_cmd('half')
   d2 = DiskCmd()
   d2.ops_disk_cmd()