#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 19:07
# @Author  : hyang
# @File    : ssh_utils.py
# @Software: PyCharm

import os
import sys

import paramiko
from colorama import Fore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from conf import settings
from utils import unicode_utils



class SSHConnection(object):

    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.pwd = host_dict['pwd']
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        """
         执行shell命令,返回字典
         return {'color': 'red','res':error}或
         return {'color': 'green', 'res':res}
        :param command:
        :return:
        """
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res = unicode_utils.to_str(stdout.read())
        # 获取错误信息
        error = unicode_utils.to_str(stderr.read())
        # 如果有错误信息，返回error
        # 否则返回res
        if error.strip():
            return {'color':'red','res':error}
        else:
            return {'color': 'green', 'res':res}

    def upload(self,local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path, confirm=True)
        # print(os.stat(local_path).st_mode)
        # 增加权限
        # sftp.chmod(target_path, os.stat(local_path).st_mode)
        sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀

    def download(self,target_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 下载至服务器 /tmp/test.py
        sftp.get(target_path, local_path)

    # 销毁
    def __del__(self):
        self.close()


if __name__ == '__main__':
    pass
    # ssh = SSHConnection(settings.host_li[0])
    # ssh.connect()
    # r1 = ssh.run_cmd('''df -h| grep  -E \([6-9][1-9]\%\)\|\(100\%\)|awk '{OFS="|"; print $2,$3,$4,$5}' ''' )
    #
    # print(Fore.RED+'%s '%r1['res'])
    #
    # res = ssh.upload('luffy.json', "/home/ap/tscms/luffy.json")


# ssh.close()

# def depoly_monitor(path='/etc/pass', line=10):
#     # 创建SSH对象
#     ssh = paramiko.SSHClient()
#     # 允许连接不在know_hosts文件中的主机
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # 连接服务器
#     ssh.connect(hostname='10.1.208.42', port=22, username='tscms', password='tscms')
#
#     # 执行命令
#     stdin, stdout, stderr = ssh.exec_command('tail -n {0} {1}'.format(line, path))
#     # 获取命令结果
#     result = stdout.read()
#     error = stderr.read()
#     print(Fore.GREEN + unicode_utils.to_str(result))
#     print(Fore.RED + unicode_utils.to_str(error))
#
#     # 关闭连接
#     ssh.close()
#
# def monitor1():
#     transport = paramiko.Transport(('hostname', 22))
#     transport.connect(username='wupeiqi', password='123')
#
#     ssh = paramiko.SSHClient()
#     ssh._transport = transport
#
#     stdin, stdout, stderr = ssh.exec_command('df')
#     print
#     stdout.read()
#
#     transport.close()
#
#
# def main():
#     # with open('hosts') as f:
#     #     for line in f:
#     depoly_monitor()
#
#
# if __name__ == '__main__':
#     # main()




# 1、pip3 install pycrypto
# 2、pip3 install crypto
# 3、pip3 install ecdsa
# 4、pip3 install paramiko
# 5、pip3 install fabric3

# [root@china ops]# fab -f fabfile.py hostname
# [10.1.208.42] Executing task 'hostname'
# [10.1.208.42] run: hostname
# [10.1.208.42] out: etl2.jkxt.sipfinfo.com
# [10.1.208.42] out:
