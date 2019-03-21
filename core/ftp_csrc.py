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
from utils.time_utils import get_curr_dt
from utils.zip_util import ZFile
import re
from utils import my_logset
from utils.oracle_utils import Ora_util
from utils.ftp_util import FTP_OPS

re_csrc = r'^SC_\d{8}_\d{8}_\d+N_A01|A02|A03|A04|A05|A06|A07|A08|A09|A10|A11|A12|A13_Z\.TXT$'
# 压缩文件名正则匹配串

CSRC_TABLE = 'CSDC_FILE_SEND_LOG'


# 监控表

# ftp连接参数
# FTP_IP = '172.16.2.113'
# FTP_PORT = '21'
# FTP_USER = 'ipfput'
# FTP_PWD = 'ipfput888'

FTP_IP = '10.1.208.41'
FTP_PORT = 21
FTP_USER = 'tscms'
FTP_PWD = 'tscms'


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


def is_workdt(today:str):
    """
    判断今日是否为工作日
    :return:
    """
    sql = "SELECT  COUNT(1) from pub_work_date where work_date_sta !=0 and  work_date =:work_date"
    csrc_ora = Ora_util()  # 数据库对象
    res = csrc_ora.queryBySql(sql,{'work_date':today})  # 查询
    return res



def insert_csrc(file_list: list):
    """
    插入文件列表
    :param file_list:
    :return:
    """

    column = ['FILE_NAME', 'ST_DATE']
    csrc_ora = Ora_util()  # 数据库对象
    try:
        rows = csrc_ora.insertMany(table=CSRC_TABLE, columns=column,values=file_list)
        if rows > 0:
            csrc_ora.commit()
            csrc_log_obj.info('插入CSDC_FILE_SEND_LOG表记录数[%s]' % (rows))
    except Exception as e:
        csrc_log_obj.error(e)
        csrc_ora.rollback()


def del_csrc(dt):
    """
    删除记录
    :param dt: 数据日期
    :return:
    """
    col_dict = { 'ST_DATE':dt}
    csrc_ora = Ora_util()  # 数据库对象
    try:
        rows = csrc_ora.deleteByTable(table=CSRC_TABLE,cond_dict=col_dict )
        if rows > 0:
            csrc_ora.commit()
            csrc_log_obj.info('删除CSDC_FILE_SEND_LOG表记录数[%s]' % (rows))
    except Exception as e:
        csrc_log_obj.error(e)
        csrc_ora.rollback()


def update_csrc(col_dict: dict, where_dict: dict):
    """
    修改文件状态
    :param col_dict: 修改列
    :param where_dict: where条件
    :return:
    """
    csrc_ora = Ora_util()  # 数据库对象
    try:
        rows = csrc_ora.updateByTable(
            table=CSRC_TABLE,
            column_dict=col_dict,
            cond_dict=where_dict)
        if rows > 0:
            csrc_ora.commit()
            csrc_log_obj.info('修改CSDC_FILE_SEND_LOG表记录数[%s]' % (rows))
    except Exception as e:
        csrc_log_obj.error(e)
        csrc_ora.rollback()


def zip_file(src:str, dst:str, file_li: list):
    """
    压缩文件
    :param src: 源目录
    :param dst: 目标目录
    :param file_li: 文件列表
    :return:
    """
    zf = ZFile(CSRC_LOG_FILE)

    executor = ThreadPoolExecutor(12, 'thread')  # 线程池
    start = time.time()
    if os.path.isdir(src):  # 判断是否为目录
        os.chdir(src)
        res = []  # 返回结果
        if not os.path.exists(dst):
            os.makedirs(dst)
        for file in file_li: # 遍历所有文件，
            file_prefix = os.path.splitext(
                os.path.join(src, file))  # 得到文件前缀和后缀名
            if len(file_prefix) > 1 and 'TXT' in file_prefix[1]:
                future = executor.submit(zf.zip_file,
                                         file, '%s.zip' %
                                         os.path.splitext(
                                             os.path.join(
                                                 dst, file))[0])  # 异步提交任务压缩文件

                res.append(future)
        executor.shutdown()  # 等待所有线程执行完毕
        print("++++>")
        for r in res:
            print(r.result())  # 打印结果
            if r.result().get('flag'):
                update_csrc({'FILE_COMPRE_FLG':'S'},{'FILE_NAME': r.result().get('file_name')})
            else:
                update_csrc({'FILE_COMPRE_FLG': 'F'}, {'FILE_NAME': r.result().get('file_name')})

    else:
        csrc_log_obj.warn('目录不存在[{}]'.format(src))
    end = time.time()
    print(end - start)


def filter_file(dir:str,tp:str):
    """
    过滤文件，生成文件列表
    :param dir:
    :param tp:
    :return:
    """
    file_li = []
    if os.path.isdir(dir):  # 判断是否为目录
        if tp == 'new':
             file_li = [file for file in os.listdir(dir) if re.search(re_csrc, file) ]  # 筛选符合规则的文件
             print(file_li)
             write_li(file_li,'csrc_{}_new.LIST'.format(dt),src_new)  # 写文件列表

        else:
             file_li = [file for file in os.listdir(dir) if re.search(r'SC\w+Z\.TXT$', file)]
             if tp == 'common':
                write_li(file_li, 'csrc_{}_common.LIST'.format(dt),src_new)
             elif tp == 'zd':
                 write_li(file_li, 'csrc_{}_zd.LIST'.format(dt), src_new)

        insert_csrc([(f, dt) for f in file_li])  # 插入数据库记录
    return file_li


def write_li(file_li:list, file_name:str, dir:str):
    """
    把列表内容写入到文件中
    :param li: 列表
    :param file_name: 文件名
    :param dir: 文件目录
    :return:
    """

    with open(os.path.join(dir,file_name), 'w') as f:
        for l in file_li:
            f.write(l)
            f.write("\n")


def ftp_upload(remote_dir,local_dir):
    """
    文件上传
    :param remote_dir:
    :param local_dir:
    :param file_li:
    :return:
    """
    ftp_obj = FTP_OPS(CSRC_LOG_FILE,FTP_IP,FTP_PORT,FTP_USER,FTP_PWD)
    ftp_executor = ThreadPoolExecutor(2, 'ftp_thread')  # 线程池
    start = time.time()
    if os.path.isdir(local_dir):  # 判断是否为目录
        os.chdir(local_dir)
        res = []  # 返回结果
        for file in os.listdir(local_dir):  # 遍历所有文件，
            file_prefix = os.path.splitext(
                os.path.join(local_dir, file))  # 得到文件前缀和后缀名
            if len(file_prefix) > 1 and 'zip' in file_prefix[1]:
                ftp = ftp_obj.ftp_connect()
        #         print(ftp)
                future = ftp_executor.submit(ftp_obj.upload_file,
                                             ftp, remote_dir, local_dir, file)  # 异步提交任务压缩文件

                res.append(future)
        ftp_executor.shutdown()  # 等待所有线程执行完毕
        print("++++>")
        for r in res:
            print(r.result())  # 打印结果
            if r.result().get('flag'):
                update_csrc({'file_send_flg': 'S'}, {'file_name': r.result().get('file_name')})
            else:
                update_csrc({'file_send_flg': 'F'}, {'file_name': r.result().get('file_name')})

        end = time.time()
        print(end - start)




def main():

    # cs_new_li = filter_file(src_new, 'new')  # 获得文件列表
    # cs_com_li = filter_file(src_new, 'common')  # 获得文件列表
    # cs_zd_li = filter_file(src_new, 'zd')  # 获得文件列表
    del_csrc(dt)
    file_li = filter_file(src_new,'new')
    zip_file(src_new,'F://test/data/data/upload/',file_li)

    ftp_upload('test222','F://test/data/data/upload/')



if __name__ == '__main__':
    #main()
    # li = ['abd.pdf','123.fil','ww.1']
    curr_dt = get_curr_dt  # 得到当前日期

    dt = get_dt()[0].get('dt')  # 得到数据日期
    mm = dt[4:6]
    year = dt[0:4]
    day = dt[6:8]

    CSRC_LOG_FILE = 'test_csrc_%s.log' % dt
    # 日志文件
    csrc_log_obj = my_logset.get_mylogger("csrc", logfile=CSRC_LOG_FILE)
    # 日志对象
    src_new = 'F://test/data/data/10620000/'
    # src_new = '/bk/{}/{}/{}/NEW/'.format(mm, year, day)
    src_dt = '{}/zd/'.format(src_new)
    src_com = '{}/common/'.format(src_new)
    dest_dir = '/IPF/{}/{}/{}/'.format(mm, year, day)
    cl_dir = '{}/cl/'.format(src_new)

    # 读取文件目录
    csrc_log_obj.info(dt)
    csrc_log_obj.info(src_new)
    csrc_log_obj.info(src_dt)
    csrc_log_obj.info(src_com)
    csrc_log_obj.info(dest_dir)
    csrc_log_obj.info(cl_dir)
    main()
    # write_li(li,'1.txt','F://test/data/')
    # filter_list()
