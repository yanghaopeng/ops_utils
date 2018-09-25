#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 16:51
# @Author  : hyang
# @File    : rm_ext_file.py
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


root_path = '/root/files/'  # 要删除文件根目录
tail_path = ['zzjc', 'zd']   # 要删除文件上级目录名
tail_prefix = '.zip'           # 要删除文件的后缀
rm_log = my_logset.get_mylogger("rm-ext-file")
init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复

# 增加参数
parser = argparse.ArgumentParser(
    description="删除zip文件,使用rm_ext_file 年月(如201809)")

parser.add_argument("dt", type=str,
                    help="请输入年月，如201808: ")

args = parser.parse_args()


def is_inpath(path_dir):
    '判断路径是否在指定字符'
    for t in tail_path:
        if t in path_dir:
            return True
    else:
        return False


def print_warn(msg):
    """
     输出警告值
    :param msg:
    :return:
    """
    print(Fore.RED + Style.BRIGHT + msg)


def get_diff_days(d1, d2):
    "获得两个日期差"
    try:
        d1_day = datetime(int(d1.strip()[:3]), int(
            d1.strip()[4:6]), int(d1.strip()[6:]))
        d2_day = datetime(int(d2.strip()[:3]), int(
            d2.strip()[4:6]), int(d2.strip()[6:]))

        return (d1_day - d2_day).days  # 350
    except ValueError:
        msg = 'Error,日期值[%s]错误' % d2
        print_warn(msg)
        return -1


dt_m = args.dt  # 获得参数值
today = time.strftime('%Y%m%d', time.localtime())
print('today is [%s]' % today)

diff_days = get_diff_days(today, dt_m + '01')  # 获得两个日期差
if re.search('2[0-2][0-9]{4}$', dt_m) is None:
    print_warn('年月格式有误')
elif diff_days == -1:
    print_warn('日期格式有误')
elif diff_days < 100:
    print_warn('删除文件的开始日期[%s] 应该小于今日[%s] 100天以上' % (dt_m + '01', today))
else:
    rm_count = 0
    input_path = os.path.join(root_path, dt_m[4:], dt_m[0:4])  # 按年月拼接目录
    if os.path.isdir(input_path):
        for r, ds, files in os.walk(input_path):
            if is_inpath(r):
                rm_files = os.listdir(r)  # 循环删除文件的目录
                for f in rm_files:
                    if(f.endswith(tail_prefix)):  # 删除指定后缀文件
                        try:
                            res = os.remove(os.path.join(r, f))
                            if res is None:
                                rm_log.info(
                                    "Delete file [{}]".format(
                                        os.path.join(
                                            r, f)))
                                rm_count += 1
                        except Exception as e:
                            print(
                                'delete file [ %s ] fail ' %
                                os.path.join(
                                    r, f), e)

        else:
            rm_log.info('Delete files count [%s]' % rm_count)
    else:
        print_warn('目录[%s]不存在!' % input_path)
