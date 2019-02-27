#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 15:37
# @Author  : hyang
# @File    : ftp_csrc.py
# @Software: PyCharm

"""
传输中登文件
"""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.oracle_utils import Ora_util
from utils import my_logset
from utils.time_utils import run_time
from utils.zip_util import ZFile

def zip_file(dt:str, log_file):
    """
    压缩文件
    :param dt: 数据日期
    :param log_file: 日志文件名
    :return:
    """
    zf = ZFile(log_file)
    dir = 'F://test/data/%s/'%dt
    print('zipdir ',dir)
    executor = ThreadPoolExecutor(10, 'thread')  # 线程池
    start = time.time()
    if os.path.isdir(dir):  # 判断是否为目录
        os.chdir(dir)
        for file in os.listdir(
                dir):  # 遍历目录下所有文件，
            file_prefix = os.path.splitext(
                os.path.join(dir, file))  # 得到文件前缀和后缀名
            if len(file_prefix) > 1 and 'TXT' in file_prefix[1]:
                # zf.zip_file(
                #     file, '%s.ZIP' %
                #     os.path.splitext(
                #         os.path.join(
                #             dir, file))[0])  # 压缩文件
                future = executor.submit(zf.zip_file,
                                         file, '%s.ZIP' %
                                         os.path.splitext(
                                             os.path.join(
                                                 dir, file))[0])  # 异步提交任务
        executor.shutdown()  # 等待所有线程执行完毕
        print("++++>")

    end = time.time()
    print(end - start)

def main():
    print('参数个数为:{}'.format(len(sys.argv)))
    print('参数列表为:{}'.format(str(sys.argv)))
    if len(sys.argv) != 2:
        print('参数个数错误，ftp_csrc.py 数据日期(如20190101)')
        sys.exit(1)
    else:
        zip_file(sys.argv[1], 'test_zip.log')


if __name__ == '__main__':
    main()