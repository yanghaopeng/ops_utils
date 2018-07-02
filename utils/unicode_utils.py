#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 17:21
# @Author  : hyang
# @File    : unicode_utils.py
# @Software: PyCharm

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

def to_bytes(bytes_or_str):
    """
    把str类型转换为bytes
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value
