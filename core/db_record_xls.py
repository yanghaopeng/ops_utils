#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/4 15:53
# @Author  : hyang
# @File    : db_record_xls.py
# @Software: PyCharm

import records
import os
import sys
import tablib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from conf import records_db_set



os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# 设置中文
db = records.Database(records_db_set.BDDB)
params = {'userid':'1111'}
sql = '''SELECT userid as "用户ID",username as "用户名称" FROM M_USER where userid > :userid '''
xls_name='user.xls'



def export_recods(db, xls_name, sql, **kwargs):
    """
    导出数据库记录保存为xls形式
    :param db: db对象
    :param xls_name: xls_name文件名
    :param sql: sql语句
    :param kwargs: where条件
    :return:
    """
    # headers为excel 表头
    # title 为sheet名称
    dataset = tablib.Dataset(headers=['用户ID', '用户名称'], title='用户表')

    rows = db.query(query=sql, fetchall=True, **kwargs)
    for k in rows.as_dict():
        print(k.values())
        dataset.append(k.values())

    with open(xls_name, 'wb') as f:
        f.write(dataset .export(format='xls',))

export_recods(db,xls_name,sql,**params)


