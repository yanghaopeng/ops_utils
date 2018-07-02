#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 14:17
# @Author  : hyang
# @File    : cmd_utils.py
# @Software: PyCharm

import subprocess
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils import unicode_utils
from utils import my_logset
# 执行cmd或shell命令#
# from multiprocessing.dummy import Pool as ThreadPool
cmd_log = my_logset.get_mylogger("run_cmd")

def cmd_exec(cmd):
    """
     执行shell命令
     返回命令返回值和结果
    :param cmd:
    :return:
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    cmd_log.debug('run cmd:[%s]' % cmd)
    stdout, stderr = p.communicate()
    # print("stdout",stdout)
    if p.returncode != 0:
        return {'code':p.returncode, 'res':unicode_utils.to_str(stderr)}
    else:
        return {'code':p.returncode, 'res':unicode_utils.to_str(stdout)}


if __name__ == '__main__':
    pass
    cmd_list = []
    import os
    os.chdir('/root/javaapp/prop')  # 切换路径
    cmd_list.append('nohup java -Xmx1g -jar tscms_fileprocess.jar > output.log 2>&1 &')
    for cmd in cmd_list:
        p = cmd_exec(cmd)
        print(p)


    # cmd_list =[]
    # cmd_list.append('df -h')
    # cmd_list.append('ps -ef|grep jav1a|grep -v grep')
    # cmd_list.append('ps -ef|grep "pol"')
    # cmd_list.append('sh /root/ops/sum.sh')
    # # print(cmd_exec(cmd))
    # # Make the Pool of workers
    # pool = ThreadPool(4)
    # # Open the urls in their own threads
    # # and return the results
    # results = pool.map(cmd_exec, cmd_list)
    # # close the pool and wait for the work to finish
    # print(results)
    # pool.close()
    # pool.join()

