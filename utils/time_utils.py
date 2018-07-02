#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 13:28
# @Author  : hyang
# @File    : time_utils.py
# @Software: python_utils


import time
from datetime import datetime
from functools import wraps

from utils import my_logset

log = my_logset.get_mylogger("runtime")


# 返回当前日期
def get_curr_dt():
    return time.strftime('%Y%m%d',time.localtime())


# 返回当前时间
def get_curr_time():
    return time.strftime('%H%M%S', time.localtime())


# 返回两个日期相差天数
# 使用getdiffdays('20180901','20181009')
def get_diff_days(d1, d2):
    try :
        d1_day = datetime(int(d1.strip()[:3]), int(d1.strip()[4:6]), int(d1.strip()[6:]))
        d2_day = datetime(int(d2.strip()[:3]), int(d2.strip()[4:6]), int(d2.strip()[6:]))
        return (abs(d1_day - d2_day).days)  # 350
    except ValueError as e:
        print('Error,日期值错误',e)


def is_valid_date(s):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(s, "%Y%m%d")
        return True
    except ValueError:
        return False


def run_time(func):
    """
    计算程序运行时间的装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def decor(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        end = time.time()
        log.debug("func {%s} run {%10.4f}s " % (func.__name__,(end - start)))
        return res

    return decor


if __name__ == '__main__':
    @run_time
    def f1(n):
        y = 1
        x = 1
        while x <= n:
            y += x
            x += 1

        return y


    print(f1(80000))
    print(get_curr_time())
    # print(getdiffdays('201a', '20180630'))