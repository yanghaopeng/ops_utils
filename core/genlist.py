#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/14 9:09
# @Author  : hyang
# @File    : genlist.py
# @Software: PyCharm
# 生成银行list文件
import os
import sys
import time
import argparse
import glob


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.time_utils import get_curr_dt

import re
from utils import my_logset
from utils.oracle_utils import Ora_util
# from core.data_flow import DataFlow

bank_path = '/tscms_datafiles/{}/{}'
# data_f = DataFlow()
ora = Ora_util()  # 数据库对象


def find_KeyFile(file_path):
    """
    找到keyfile名字
    :return:
    """
    os.chdir(file_path)
    for file in glob.glob("*.KEY"):
        print(file)


def find_ListFile(file_path):
    """
    找到ListFile名字
    :return:
    """
    os.chdir(file_path)
    return glob.glob("*.LIST")[-1]


def insert_record(list_file, bank_path, bank_code):
    """
    插入记录
    :param list_file:
    :param bank_path:
    :param bank_code:
    :return:
    """
    insert_sql = '''
    INSERT INTO t_deal_status
       (s_id,file_name,path,uploaduser,submit_org_id,data_time,deal_start_time,status,file_length,file_version,file_type)
       VALUES (SEQ_DEAL_STATUS.NEXTVAL,'%s','%s','%s','%s','%s',sysdate,2,0,'1','3')
       ''' % (list_file, bank_path, bank_code, bank_code, get_curr_dt())

    ora.execute(sql=insert_sql)
    print('insert %s rows' % ora.get_rows_num())
    ora.commit()
    print('插入数据成功')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dt", type=str, help="date")
    parser.add_argument(
        "--bank",
        type=str,
        help="bank_code",
        default='3136020')
    args = parser.parse_args()
    print('dt:{}  bank_code:{}'.format(args.dt, args.bank))
    dt = args.dt  # 数据日期
    bank_code = args.bank  # 银行代码
    bank_path = bank_path.format(bank_code, dt)
    print('bank_path:{}'.format(bank_path))

    list_file = find_ListFile('F://test/data/1021000/')
    insert_record(list_file, bank_path, bank_code)
