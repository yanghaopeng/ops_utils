#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/2 10:13
# @Author  : hyang
# @File    : color_log.py
# @Software: PyCharm

import os
import logging
from logging import handlers
from colorama import Fore, Style, init
from conf import settings


class Colorlog(object):
    """
    记录日志，添加颜色
    """
    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复

    # 根据信息不同设置不同的颜色格式
    info_color = Fore.GREEN + Style.BRIGHT
    warn_color = Fore.YELLOW + Style.BRIGHT
    debug_color = Fore.MAGENTA + Style.BRIGHT
    error_color = Fore.RED + Style.BRIGHT

    def __init__(self, name):
        # 日志格式
        log_format = '[%(asctime)s - %(levelname)s - %(name)s] %(message)s '
        self.logger = logging.getLogger(name)
        self.logger.setLevel(settings.LOG_LEVEL)

        console_handler = logging.StreamHandler()
        # 文件绝对路径
        logfile_path = os.path.join(settings.LOG_DIR, "log", settings.COLOR_LOG_FILE)
        if not os.path.exists(os.path.join(settings.LOG_DIR, "log")):
            # 创建log目录
            os.mkdir(os.path.join(settings.LOG_DIR, "log"))
        # 每天创建一个日志文件，文件数不超过20个
        file_handler = handlers.TimedRotatingFileHandler(
            logfile_path, when="D", interval=1, backupCount=20)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        file_format = logging.Formatter(fmt=log_format)
        console_format = logging.Formatter(
            fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S ')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

    def warn(self, message):
        self.logger.warning(Colorlog.warn_color + message)

    def info(self, message):
        self.logger.info(Colorlog.info_color + message)

    def error(self, message):
        self.logger.error(Colorlog.info_color + message)

    def debug(self, message):
        self.logger.debug(Colorlog.info_color + message)


if __name__ == '__main__':
    cp_log = Colorlog("cp")