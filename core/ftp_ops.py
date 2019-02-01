#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/4 19:42
# @Author  : hyang
# @File    : ftp_ops.py
# @Software: PyCharm

"""
FTP常用操作
"""
from ftplib import FTP
from ftplib import error_perm
import os
import socket
import time
from utils import file_util


class FTP_OPS(object):
    def __init__(self, host, username, password, port):
        """
        初始化ftp
        :param host: ftp主机ip
        :param username: ftp用户名
        :param password: ftp密码
        :param port:  ftp端口 （默认21）
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def ftp_connect(self):
        """
        连接ftp
        :return:
        """
        ftp = FTP()
        ftp.encoding = 'utf-8'
        ftp.set_debuglevel(2)  # 开启调试模式
        try:
            ftp.connect(host=self.host, port=self.port)  # 连接ftp
            ftp.login(self.username, self.password)  # 登录ftp
            print(ftp.getwelcome())  # 打印欢迎信息
        except(socket.error, socket.gaierror):  # ftp 连接错误
            print("ERROR: cannot connect [{}:{}]".format(host, port))
            return None

        except error_perm:  # 用户登录认证错误
            print("ERROR: user Authentication failed ")
            return None
        return ftp

    def download_file(self, ftp_file_path, dst_file_path):
        """
        从ftp下载文件到本地
        :param ftp_file_path: ftp下载文件
        :param dst_file_path: 本地存放
        :return:
        """
        buffer_size = 10240  # 默认是8192
        ftp = self.ftp_connect()
        print(ftp.getwelcome()) #显示登录ftp信息

        # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
        ftp.voidcmd('TYPE I')
        remote_file_size = ftp.size(ftp_file_path)  # 文件大小

        print('remote filesize [{}]'.format(remote_file_size))
        cmpsize = 0
        lsize = 0
        # check local file isn't exists and get the local file size
        if os.path.exists(dst_file_path):
            lsize = os.stat(dst_file_path).st_size
        if lsize >= remote_file_size:
            print('local file is bigger or equal remote file')
            return
        start = time.time()
        conn = ftp.transfercmd('RETR {0}'.format(ftp_file_path), lsize)

        f = open(dst_file_path, "ab")
        while True:
            data = conn.recv(buffer_size)
            if not data:
                break
            f.write(data)
            cmpsize += len(data)
            print(
                 '\b'*30, 'download process:%.2f%%' %
                (float(cmpsize) / remote_file_size * 100))
            # ftp.retrbinary(
            #     'RETR {0}'.format(ftp_file_path),
            #     f.write,
            #     buffer_size)
        f.close()
        try:
            ftp.voidcmd('NOOP')
            print('keep alive cmd success')
            ftp.voidresp()
            print('No loop cmd')
            conn.close()
            ftp.quit()
        except Exception as e:
            pass
        finally:
            end = time.time()
            print('consume time [{}]'.format(end - start))
            file_size = os.stat(dst_file_path).st_size
            print('local filesize [{}] md5:[{}]'.format(
                file_size, file_util.get_md5(dst_file_path)))



if __name__ == '__main__':
    host = "10.0.0.1"
    username = "test"
    password = "test"
    port = "21"
    ftp_file_path = "/data/an/1.zip"
    dst_file_path = "/data/tmp/1.zip"
    ftp = FTP_OPS(host=host, username=username, password=password, port=port)
    ftp.download_file(ftp_file_path=ftp_file_path, dst_file_path=dst_file_path)
