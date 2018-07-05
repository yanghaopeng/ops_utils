#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/5 12:55
# @Author  : hyang
# @File    : db_check.py
# @Software: PyCharm

import os
import sys
from colorama import init, Fore, Style

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.oracle_utils import Ora_util
from utils import my_logset
from conf import settings
from conf import db_set
from utils.time_utils import is_valid_date
from utils.time_utils import get_curr_time
from conf.settings import cc_dir
from utils import cmd_utils
from utils.print_log import print_info, print_debug, print_error
from prettytable import PrettyTable
from prettytable import from_db_cursor


class DbCheck(object):
    def __init__(self, db_info=settings.prod_db):
        # 日志
        init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
        # self.df_log = my_logset.get_mylogger("db_check",'db.log')
        self.ora = self.__get_Ora(db_info)

    @staticmethod
    def __get_Ora(db_info):
        return Ora_util(db_info)

    def catTableSpace(self):
        # table_dict = self.ora.queryBySql(
        #     db_set.table_sql)
        # if table_dict:

        tb = from_db_cursor(self.ora.execute(db_set.table_sql))
        # 设定左对齐
        tb.align = 'l'
        # 设定T_ID右对齐
        # tb.align["FREE"] = "r"
        # tb.align["USED"] = "r"
        # tb.align["AVAIL"] = "r"
        # 设定数字输出格式
        tb.float_format = "2.2"
        # 设定边框连接符为'*"
        tb.junction_char = "*"
        # 设定排序列
        # tb.sortby = "AVAIL"
        # 设定排序方式
        # tb.reversesort = True
        # 设定左侧不填充空白字符
        tb.left_padding_width = 0
        print_info('查询数据库表空间')
        print(tb)


if __name__ == '__main__':
    db1 = DbCheck()
    db1.catTableSpace()
