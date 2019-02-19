#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/1 13:02
# @Author  : hyang
# @File    : cp_deploy.py
# @Software: PyCharm

import os
import shutil
import sys
import subprocess


def get_dir_size_count(dir):
    """
    获得文件夹中所有文件大小和文件个数
    :param dir:
    :return:
    """
    print('开始计算…… ')
    size = 0
    count = 0
    for root, dirs, files in os.walk(dir):
        size_li = [os.path.getsize(os.path.join(root, name))
                   for name in files]
        size += sum(size_li)
        count += len(size_li)
        print('目录{}  文件个数{}， 总共大小约{}'.format(dir, count, bytes2human(size)))
    return count, bytes2human(size)


def upload_file(src_path, dst_path):
    """
    上传文件
    :param src_path:
    :param dst_path:
    :return:
    """
    print('upload_file %s   %s' % (src_path, dst_path))
    # 目标目录是否存在，不存在则创建
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
        print('Create Dest Dir %s' % dst_path)

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
                    print('Create Dest Dir %s' % dst_path)

                shutil.copy(local_file_path, dst_file_path)  # copy file
                print('copy to file {} complete '.format(dst_file_path))
                all_file_nums += 1

                print(
                    'copy all files complete , files count = {}'.format(all_file_nums))
    else:
        print('Dir is not exists %s' % dst_path)


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


def cmd_exec(cmd):
    """
     执行shell命令
     返回命令返回值和结果
    :param cmd:
    :return:
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print('run cmd:[%s]' % cmd)
    stdout, stderr = p.communicate()
    # print("stdout",stdout)
    if p.returncode != 0:
        return {'code': p.returncode, 'res': to_str(stderr)}
    else:
        return {'code': p.returncode, 'res': to_str(stdout)}


def to_str(bytes_or_str):
    """
    把byte类型转换为str
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value


if __name__ == '__main__':
    src = cmd_exec("pwd")['res'].strip()  # 源目录
    dst = '/home/copytest2'  # 目标目录
    upload_file(src, dst)
    get_dir_size_count(src)
