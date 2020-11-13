#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 8:44
# @Author  : hyang
# @File    : zzjc_hiscp.py
# @Software: PyCharm


import os
import re
import sys
import time
from datetime import datetime
from colorama import init, Fore, Style
import argparse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils import my_logset
from utils import file_util
from utils import dealIni

# zzjc配置
FILE_DT = dealIni.readZzjc("file_dt")
FILE_START = dealIni.readZzjc("file_start")
FILE_END = dealIni.readZzjc("file_end")
FILE_TYPE = dealIni.readZzjc("file_type")




def cp_file():
    """
    拷贝文件
    :return:
    """
    for dt in FILE_DT.split(','):
        file_path = FILE_START
        ZZJC_LOG_FILE = 'zzjc_%s.log' % dt
        # 日志文件
        csrc_log_obj = my_logset.get_mylogger("csrc", logfile=ZZJC_LOG_FILE)
