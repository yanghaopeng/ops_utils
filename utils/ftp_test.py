#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 8:59
# @Author  : hyang
# @File    : ftp_test.py
# @Software: PyCharm

import socket
import time
from datetime import date,timedelta
from ftplib import FTP
import sys
import os

ftp_server = '10.1.208.41'

ftp_user = 'tscms'
ftp_password = 'tscms'
ftp_backup_dir = 'backup'

newday = date.today()  # 获取今天的日期
oldday = date.today() - timedelta(5)  # 获得5天前的日期
# newfile = '/home/backup/' + 'backup_data_' + str(newday.year) + '.' + str(newday.month) + '.' + str(
#     newday.day) + '.zip'  # 本次备份文件名(绝对路径)
# oldfile = '/home/backup/' + 'backup_data_' + str(oldday.year) + '.' + str(oldday.month) + '.' + str(
#     oldday.day) + '.zip'  # 5天前备份的文件名(绝对路径)

# newfile = '/home/ap/tscms/zhao_test/1.txt'
newfile = 'F:/test/data/data/upload/SC_10620000_20190308_021N_A10_Z.TXT'

def upload():
    socket.setdefaulttimeout(60)  # 超时FTP时间设置为60秒
    ftp = FTP()
    ftp.connect(host=ftp_server, port=21)
    ftp.set_debuglevel(2)  # 开启调试模式
    ftp.encoding = 'utf-8'
    print("login ftp...")
    try:
        ftp.login(ftp_user, ftp_password)
        print(ftp.getwelcome())  # 获得欢迎信息
        ftp.cwd('etc')
        try:
            if ftp_backup_dir in ftp.nlst():
                print("found backup folder in ftp server, upload processing.")
            else:
                print("don't found backup folder in ftp server, try to build it.")
                ftp.mkd(ftp_backup_dir)
        except:
            print("the folder" + ftp_backup_dir + "doesn't exits and can't be create!")
            sys.exit()
    except:
        print("ftp login failed.exit.")
        sys.exit()
    ftp.cwd(ftp_backup_dir)  # 设置FTP路径

    print("upload data...")
    ftp.voidcmd('TYPE I')
    fp = open(newfile, 'rb')
    try:
        if os.path.basename(newfile) in ftp.nlst():
            ftp.delete(os.path.basename(newfile))
        print(os.path.basename(newfile))
        ftp.storbinary('STOR ' + os.path.basename(newfile), fp, 1024)  # 上传备份文件
    except Exception as e:
        print("upload failed. check your permission.",str(e))
    finally:
        fp.close()
    # print("delte old file...")
    # try:
    #     ftp.delete(os.path.basename(oldfile))  # 删除5天前的备份文件
    # except:
    #     print("the old file in ftp doesn't exists, jumped.")
    ftp.set_debuglevel(2)
    print("ftp upload successful.exit...")
    ftp.quit()


if __name__ == '__main__':
    upload()
