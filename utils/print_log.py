#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 10:18
# @Author  : hyang
# @File    : print_log.py
# @Software: PyCharm


from colorama import Fore, Style, init

"""
    记录输出，添加颜色
"""
init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复

# 根据信息不同设置不同的颜色格式
info_color = Fore.GREEN + Style.BRIGHT
warn_color = Fore.BLUE + Style.BRIGHT
debug_color = Fore.MAGENTA + Style.BRIGHT
error_color = Fore.RED + Style.BRIGHT


def print_info(message):
    print(info_color + str(message))


def print_warn(message):
    print(warn_color + str(message))


def print_debug(message):
    print(debug_color + str(message))


def print_error(message):
    print(error_color + str(message))
