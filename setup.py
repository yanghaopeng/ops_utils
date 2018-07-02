#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 23:39
# @Author  : hyang
# @File    : setup.py
# @Software:

from setuptools import setup
# import os
# import sys
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_DIR)  # 加入环境变量
setup(
    name='ops_manage',
    version='0.1',
    packages=['core', 'conf', 'utils','bin', 'db'],
    include_package_data=True,
    install_requires=[
        'Click',
        'prettytable'
    ],
    # entry_points={
    #     'console_scripts': [
    #     # 'dfcmd'='ops_manage:dfcmd',
    #     # 'catdp'='ops_manage:catdp'
    # ]},
    entry_points='''
        [console_scripts]
        dfcmd=core.ops_manage:dfcmd
        catdp=core.ops_manage:catdp
    '''
)