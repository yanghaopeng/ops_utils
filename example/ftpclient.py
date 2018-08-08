#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 17:17
# @Author  : hyang
# @File    : ftpclient.py
# @Software: PyCharm

# FTP操作
from ftplib import FTP  # 加载ftp模块

host = '127.0.0.1'
username = 'egon'
password = '123456'
file = '1.txt'
port = 2111
#
# ftp = FTP()
# ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
# ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
# ftp.connect(host, 2111)
# ftp.login(username, password)
# print(ftp.getwelcome())     # 打印欢迎信息
# print(ftp.dir() )                  # 显示目录下所有目录的信息
# ftp.quit()
# # 获取当前路径
# pwd_path = ftp.pwd()
# print("FTP当前路径:", pwd_path)



# from ftplib import FTP
# import time
# import tarfile
#
#
#
# def ftpconnect(host, username, password)
#     ftp = FTP()
#     ftp.connect(host, 21)
#     ftp.login(username, password)
#     return ftp
#
# def downloadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'wb')
#     ftp.retrbinary('RETR'+remotepath, fp.write, bufsize)
#
#     ftp.set_debuglevel(0)
#     fp.close()
#
# def uploadfile(ftp, remotepath, localpath):
#     bufsize = 1024
#     fp = open(localpath, 'rb')
#     ftp.storbinary('STOR'+remotepath, fp, bufsize)
#     ftp.set_debuglevel(0)
#     fp.close()
#
# if __name__ == '__main__':
#     ftp = ftpconnect("******", "***", "***")
#     downloadfile(ftp, "***", "***")
#     uploadfile(ftp, "***", "***")
#
#     ftp.quit()

from ftplib import FTP


def ftpconnect(host, port, username, password):
    ftp = FTP()
    ftp.set_debuglevel(2)         #打开调试级别2，显示详细信息
    ftp.encoding = 'utf-8'  # 解决中文编码问题，默认是latin-1
    ftp.connect(host, port)  # 连接
    ftp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
    print(ftp.getwelcome())  # 打印欢迎信息
    return ftp


def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024  # 设置缓冲块大小
    fp = open(localpath, 'wb')  # 以写模式在本地打开文件
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # 接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)  # 关闭调试
    fp.close()  # 关闭文件


def uploadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    ftp = ftpconnect(host, port, username, password)
    print(ftp.nlst())
    downloadfile(ftp, "cx_Oracle-6.3.1-cp36-cp36m-win_amd64.whl", "e:/x.whl")
    # uploadfile(ftp, "***", "***")
    pwd_path = ftp.pwd()
    print("FTP当前路径:", pwd_path)

    ftp.quit()