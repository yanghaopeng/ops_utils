#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 17:00
# @Author  : hyang
# @File    : ftpdemo.py
# @Software: PyCharm

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import configparser
import logging

IP = '127.0.0.1'

PORT = '2111'

# 上传速度  100kb/s
MAX_UPLOAD = 100 * 1024

# 下载速度 100kb/s
MAX_DOWNLOAD = 100 * 1024

# 最大连接数
MAX_CONS = 100

# 最多IP数
MAX_PER_IP = 10

# 被动端口范围，注意被动端口数量要比最大IP数多，否则可能出现无法连接的情况
PASSIVE_PORTS = (8300, 8500)

# 是否开启匿名访问 on|off
ENABLE_ANONYMOUS = 'off'

# 匿名用户目录
ANONYMOUS_PATH = 'E:/DEVTOOL/'


# 日志文件
LOGING_NAME = 'pyftp.log'

# 欢迎信息
WELCOME_MSG = 'Welcome to my ftp'

# 新建一个用户组
authorizer = DummyAuthorizer()

# 读取用户配置
config = configparser.ConfigParser()
config.read('user.ini')
user_list = config.sections()
for user in user_list:
    passwd = config[user]["password"]
    perm = config[user]["perm"]
    home_dir = config[user]["home"]
    # 将用户名，密码，指定目录，权限 添加到里面
    authorizer.add_user(user, passwd, homedir=home_dir, perm=perm)

# 添加匿名用户 只需要路径
if ENABLE_ANONYMOUS == 'on':
    authorizer.add_anonymous(ANONYMOUS_PATH)

# 下载上传速度设置
dtp_handler = ThrottledDTPHandler
dtp_handler.read_limit = MAX_DOWNLOAD
dtp_handler.write_limit = MAX_UPLOAD

# 初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

# 添加被动端口范围
handler.passive_ports = range(PASSIVE_PORTS[0], PASSIVE_PORTS[1])


# 欢迎信息
handler.banner = WELCOME_MSG

# 监听ip 和 端口
server = FTPServer((IP, PORT), handler)

# 最大连接数
server.max_cons = MAX_CONS
server.max_cons_per_ip = MAX_PER_IP

# 开始服务
print('FTP开始服务 ', (IP, PORT))
server.serve_forever()
