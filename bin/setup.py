#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24 23:39
# @Author  : hyang
# @File    : setup.py
# @Software:

from setuptools import setup,find_packages


setup(
    name='ops_manage',
    version='0.1',
    py_modules=['ops_manage'],
    packages=find_packages(),
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
        dfcmd=ops_manage:dfcmd
    '''
)