#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 15:38
# @Author  : hyang
# @File    : csrc_upload.py
# @Software: PyCharm

# 上传ftp 文件

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.time_utils import get_curr_dt
import re
from utils import my_logset
from utils.oracle_utils import Ora_util
from utils.ftp_util import FTP_OPS
import argparse
from utils import dealIni


# ftp连接参数
FTP_IP = dealIni.readZdFtp("IP")
FTP_PORT = dealIni.readZdFtp("PORT")
FTP_USER = dealIni.readZdFtp("USER")
FTP_PWD = dealIni.readZdFtp("PWD")

CSRC_LOG_FILE = 'test_csrc_%s.log' % get_curr_dt()


def get_dt():
    """
    得到数据日期
    :return:
    """
    sql = "select max(work_date) dt from pub_work_date where work_date_sta !=0 and  work_date < (\
            select max(work_date)\
                from pub_work_date \
                where work_date_sta !=0 and  work_date < to_char(sysdate,'YYYYMMDD'))"
    csrc_ora = Ora_util()  # 数据库对象
    res = csrc_ora.queryBySql(sql)  # 查询
    return res


def update_csrc(flg, file_name):
    """
    修改文件状态
    :param flg: 标志
    :param file_name: 文件名
    :return:
    """
    csrc_ora = Ora_util()  # 数据库对象
    try:
        update_sql = '''update CSDC_FILE_SEND_LOG set file_send_flg = '%s',file_send_time = sysdate
where file_name = '%s' ''' % (flg, file_name)
        csrc_ora.execute(update_sql)
        if csrc_ora.get_rows_num() > 0:
            csrc_log_obj.debug(
                'update %s rows' %
                csrc_ora.get_rows_num())
            csrc_ora.commit()
            csrc_log_obj.info(
                '修改CSDC_FILE_SEND_LOG表记录数[%s]' %
                (csrc_ora.get_rows_num()))
    except Exception as e:
        csrc_log_obj.error(e)
        csrc_ora.rollback()


def get_ftplist(pathname):
    """
    :return:
    """
    ftp_obj = FTP_OPS(CSRC_LOG_FILE, FTP_IP, FTP_PORT, FTP_USER, FTP_PWD)
    ftp_obj = ftp_obj.ftp_connect()
    ftp_obj.cwd(pathname)  # 切换路径
    print(ftp_obj.nlst())
    file_name = 'ftp_log_{}'.format(dt)
    with open(file_name, 'w') as file_obj:
        for f_name in ftp_obj.nlst():
            file_obj.write(f_name + '\n')
    # 将FtpServer目录下面的文件返回成一个列表


def upload_file(file_name):
    """
    上传文件
    :return:
    """
    ftp_obj = FTP_OPS(CSRC_LOG_FILE, FTP_IP, FTP_PORT, FTP_USER, FTP_PWD)
    ftp = ftp_obj.ftp_connect()
    r = ftp_obj.upload_file(
        ftp,
        remotepath=dest_dir,
        localpath=cl_dir,
        file=file_name)
    if r.get('flag'):
        update_csrc('S', r.get('file_name'))
    else:
        update_csrc('F', r.get('file_name'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dt", type=str, help="date")
    parser.add_argument("file", type=str, help="filename")
    args = parser.parse_args()
    print('dt:{}  filename:{}  '.format(args.dt, args.file))
    dt = args.dt
    # 日志文件
    csrc_log_obj = my_logset.get_mylogger("csrc", logfile=CSRC_LOG_FILE)
    mm = dt[4:6]
    year = dt[0:4]
    day = dt[6:8]
    dest_dir = '/IPF/{}/{}/{}/'.format(mm, year, day)
    src_new = '/bk/{}/{}/{}/NEW/'.format(mm, year, day)
    cl_dir = '{}/cl/'.format(src_new)
    up_file_name = args.file
    csrc_log_obj.info(
        '准备上传文件CSDC_FILE_SEND_LOG表记录[%s]' % (up_file_name))
    upload_file(file_name=up_file_name)
    # update_csrc('a.zip')
