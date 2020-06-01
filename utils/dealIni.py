#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/29 11:02
# @Author  : hyang
# @File    : dealIni.py
# @Software: PyCharm
# 处理ini文件

import os
import configparser
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from conf import settings

config = configparser.ConfigParser()


def existFile(filePath):
    """
     判断ini文件存在
    :param filePath:
    :return:
    """
    iniFile = filePath
    # 判断文件存在
    if not os.path.isfile(iniFile):
        print('ini文件不存在!')
        iniFile = None

    return iniFile


def readSec(filePath, section):
    """
    :param filePath:
    :param section: 配置段[section]
    :return:
    读取ini文件的配置段
    """

    config.read(filePath)
    sec = config.sections()
    if section not in sec:
        print('ini文件[{}]段找不到!'.format(section))
    return config.items(section)


def readOption(filePath, section, option):
    """
    读取配置项
    :param option: option=?
    :return:
    """
    value = None
    try:
        if existFile(filePath):
            config.read(filePath)
            if not config.has_option(section, option):
                print('ini文件[{}]段[{}]选项找不到!'.format(section, option))
            else:
                value = config.get(section, option)
    except Exception as e:
        print(e)
    return value


def readZdFtp(option):
    """
    读取中登ftp配置
    :param option:
    :return:
    """
    file_path = settings.zdftp_dir
    return readOption(file_path, "zdftp", option)


