#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/29 14:55
# @Author  : hyang
# @File    : cp_batch.py
# @Software: PyCharm

import os
import shutil
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.time_utils import run_time
from utils.color_log import Colorlog
from utils.print_log import print_info

cp_log = Colorlog("cp")


def get_dir_size_count(dir):
    """
    获得文件夹中所有文件大小和文件个数
    :param dir:
    :return:
    """
    size = 0
    count = 0
    for root, dirs, files in os.walk(dir):
        size_li = [os.path.getsize(os.path.join(root, name))
                   for name in files]
        size += sum(size_li)
        count += len(size_li)
    print_info('目录{}  文件个数{}， 总共大小约{}'.format(dir, count, bytes2human(size)))
    return count, bytes2human(size)


@run_time
def upload_file(src_path, dst_path):
    """
    上传文件
    :param src_path:
    :param dst_path:
    :return:
    """
    cp_log.info('upload_file %s   %s' % (src_path, dst_path))
    # 目标目录是否存在，不存在则创建
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
        cp_log.info('Create Dest Dir %s' % dst_path)

    # 判断是否为目录，存在则把文件拷贝到目标目录下
    if os.path.isdir(src_path):
        all_file_nums = 0
        for root, dirs, files in os.walk(src_path):
            # 遍历目录下所有文件根，目录下的每一个文件夹(包含它自己),
            # 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名称】
            for f in files:
                local_file_path = os.path.join(root, f)  # 本地文件路径 如/src/q.txt
                dst_file_path = os.path.abspath(
                    local_file_path.replace(
                        src_path, dst_path))  # 目标文件路径 如/dst/q.txt
                dst_dir = os.path.dirname(dst_file_path)  # 目标文件路径文件夹 如/dst/
                if not os.path.isdir(dst_dir):
                    os.makedirs(dst_dir)  # 创建目录
                    cp_log.debug('Create Dest Dir %s' % dst_path)

                shutil.copy(local_file_path, dst_file_path)  # copy file
                cp_log.debug('copy to file {} complete '.format(dst_file_path))
                all_file_nums += 1

        cp_log.info(
            'copy all files complete , files count = {}'.format(all_file_nums))
    else:
        cp_log.warn('Dir is not exists %s' % dst_path)


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E')
    prefix = {}
    for i, s in enumerate(symbols):
        # << 左移” 左移一位表示乘2 即1 << 1=2，二位就表示4 即1 << 2=4，
        # 10位就表示1024 即1 << 10=1024 就是2的n次方
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f%s' % (value, s)
    return "%sBytes" % n


if __name__ == '__main__':
    src = 'D://test1'
    dst = 'D://copytest2'
    upload_file(src, dst)
    print_info(get_dir_size_count(dst))
