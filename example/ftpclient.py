#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 17:17
# @Author  : hyang
# @File    : ftpclient.py
# @Software: PyCharm



# FTP操作
from ftplib import FTP  # 加载ftp模块
from ftplib import error_perm
from utils import file_util
import os
import time
import socket
from concurrent.futures import ThreadPoolExecutor

host = '127.0.0.1'
username = 'egon'
password = '123456'
file = '1.txt'
port = 2111


def ftpconnect(host, port, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
    try:
        ftp.connect(host, port)  # 连接
        ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
        print(ftp.getwelcome())  # 打印欢迎信息
    except(socket.error, socket.gaierror):  # ftp 连接错误
        print("ERROR: cannot connect [{}:{}]" .format(host, port))
        return None
    except error_perm:  # 用户登录认证错误
        print("ERROR: user Authentication failed ")
        return None
    return ftp


def is_ftp_file(ftp_conn, ftp_path):
    try:
        if ftp_path in ftp_conn.nlst(os.path.dirname(ftp_path)):
            return True
        else:
            return False
    except error_perm:
        return False


def downloadfile(ftp, remotepath, localpath):
    """
     下载文件
    :param ftp:
    :param remotepath:
    :param localpath:
    :return:
    """
    bufsize = 1024  # 设置缓冲块大小
    fp = open(localpath, 'wb')  # 以写模式在本地打开文件

    res = ftp.retrbinary(
        'RETR ' + remotepath,
        fp.write,
        bufsize)  # 接收服务器上文件并写入本地文件
    if res.find('226') != -1:
        print('download file complete', localpath)
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


def uploadfile(ftp, remotepath, localpath):
    """
    上传文件
    :param ftp:
    :param remotepath:
    :param localpath:
    :return:
    """
    bufsize = 1024
    fp = open(localpath, 'rb')
    res = ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    if res.find('226') != -1:
        print('upload file complete', remotepath)
    ftp.set_debuglevel(0)
    fp.close()


def ftp_theadpool(func, ftp, file_list):
    """
    通过线程池调用上传文件列表
    :param func:
    :param file_list:
    :return:
    """
    pool = ThreadPoolExecutor(6)
    for remotepath, localpath in file_list:
        pool.submit(func, ftp, remotepath, localpath)
    pool.shutdown()


if __name__ == "__main__":
    ftp = ftpconnect(host, port, username, password)
    file_list = ftp.nlst()
    print(file_list)
    # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
    # mode错误
    ftp.voidcmd('TYPE I')
    file_size = ftp.size("sqldeveloper-3.1.07.42.zip")  # 文件大小

    print('filesize [{}]'.format(file_util.bytes2human(file_size)))
    start = time.time()
    downloadfile(ftp, "sqldeveloper-3.1.07.42.zip", "e:/x.zip")
    end = time.time()
    print('consume time [{}]'.format(end - start))

    if '20180910' not in file_list:  # 创建目录
        res = ftp.mkd('20180910')
        print('mk ', res)


    ftp.cwd('20180910')  # 进入到新目录
    print("FTP当前路径:", ftp.pwd())
    print("文件信息:", ftp.nlst())

    uploadfile(ftp, "testup.zip", "e:/x.zip") # 上传文件
    # ftp.cwd('20180910')
    # pwd_path = ftp.pwd()
    # print("FTP当前路径:", pwd_path)
    # print("文件信息:", ftp.nlst())
    ftp.quit()
