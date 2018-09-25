#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 21:07
# @Author  : hyang
# @File    : file_util.py
# @Software: python_utils

import os
import hashlib


def bytes2human(n):
    # 文件大小字节单位转换
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
    return "%sB" % n


def get_md5(file_path):
    """
    得到文件MD5
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
        md5_obj = hashlib.md5()  # hashlib
        f = open(file_path, 'rb')  # 打开文件
        read_size = 0
        while read_size < file_size:
            read_byte = f.read(8192)
            md5_obj.update(read_byte)  # update md5
            read_size += len(read_byte)
        hash_code = md5_obj.hexdigest()  # get md5 hexdigest
        f.close()
        print('file: [{}] \nsize: [{}] \nmd5: [{}]'.format(
            file_path, bytes2human(read_size), hash_code))
        return str(hash_code)


def get_filemd5(file_path):
    # 使用迭代器读取文件获得MD5
    if os.path.isfile(file_path):
        file_size = os.stat(file_path).st_size
        md5_obj = hashlib.md5()  # hashlib
        f = open(file_path, 'rb')  # 打开文件
        read_size = 1024
        for chunk in iter(lambda: f.read(read_size), b''):  # 使用迭代器读取文件获得MD5
            md5_obj.update(chunk)
        hash_code = md5_obj.hexdigest()  # get md5 hexdigest
        f.close()
        print('file: [{}] \nsize: [{}] \nmd5: [{}]'.format(
            file_path, bytes2human(file_size), hash_code))
        return str(hash_code)


if __name__ == '__main__':

    md5 = get_md5(
        r'C:\Users\china\PycharmProjects\sfa_tj\README.md')
    md5_1 = get_filemd5(
        r'C:\Users\china\PycharmProjects\sfa_tj\README.md')
