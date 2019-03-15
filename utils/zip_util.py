#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 15:07
# @Author  : hyang
# @File    : zip_util.py
# @Software: PyCharm

import zipfile
import os.path
import os
from utils import my_logset
from utils.time_utils import run_time
from threading import currentThread


class ZFile(object):
    """
    文件压缩
    """

    def __init__(self, log_file):
        self.db_log = my_logset.get_mylogger("zip", log_file)

    @run_time
    def zip_file(self, fs_name, fz_name):
        """
        从压缩文件
        :param fs_name: 源文件名
        :param fz_name: 压缩后文件名
        :return:
        """
        flag = False
        if fs_name and fz_name:
            try:
                with zipfile.ZipFile(fz_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(fs_name)
                    print(
                        "%s is running [%s] " %
                        (currentThread().getName(), fs_name))
                    self.db_log.info('压缩文件[{}]成功'.format(fs_name))
                if zipfile.is_zipfile(fz_name):
                    os.remove(fs_name)
                    self.db_log.info('删除文件[{}]成功'.format(fs_name))
                flag = True
            except Exception as e:
                self.db_log.error('压缩文件[{}]失败'.format(fs_name), str(e))

        else:
            print('文件名不能为空')
        return {'file_name': fs_name, 'flag': flag}

    def unzip_file(self, fz_name, path):
        """
        解压缩文件
        :param fz_name: zip文件
        :param path: 解压缩路径
        :return:
        """
        flag = False
        try:
            if zipfile.is_zipfile(fz_name):  # 检查是否为zip文件
                with zipfile.ZipFile(fz_name, 'r') as zipf:
                    for p in zipf.namelist():
                        zipf.extract(p, path)  # 解压缩文件
                    print(
                        "%s is running [%s] " %
                        (currentThread().getName(), fz_name))
                    self.db_log.info('解压缩文件[{}]成功'.format(fz_name))
                flag = True
        except Exception as e:
            self.db_log.error('解压缩文件[{}]失败'.format(fz_name), str(e))
        return {'file_name': fz_name, 'flag': flag}


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    from threading import currentThread
    import os
    import time
    import random
    zf = ZFile('zip_test.log')
    # os.chdir('F:\test\data20180206\14120000\test')
    dir = 'F://test/data/20180206/'
    executor = ThreadPoolExecutor(10, 'thread')  # 线程池
    start = time.time()
    if os.path.isdir(dir):  # 判断是否为目录
        os.chdir(dir)
        for file in os.listdir(
                dir):  # 遍历目录下所有文件，
            file_prefix = os.path.splitext(
                os.path.join(dir, file))  # 得到文件前缀和后缀名
            if len(file_prefix) > 1 and 'TXT' in file_prefix[1]:
                # zf.zip_file(
                #     file, '%s.ZIP' %
                #     os.path.splitext(
                #         os.path.join(
                #             dir, file))[0])  # 压缩文件
                future = executor.submit(zf.zip_file,
                                         file, '%s.ZIP' %
                                         os.path.splitext(
                                             os.path.join(
                                                 dir, file))[0])  # 异步提交任务
        executor.shutdown()  # 等待所有线程执行完毕
        print("++++>")

    end = time.time()
    print(end - start)
    # if os.path.isdir(dir):  # 判断是否为目录
    #     os.chdir(dir)
    #     for file in os.listdir(
    #             dir):  # 遍历目录下所有文件，
    #         file_prefix = os.path.splitext(
    #             os.path.join(dir, file))  # 得到文件前缀和后缀名
    #         if len(file_prefix) > 1 and 'ZIP' in file_prefix[1]:
    #             zf.unzip_file(file, dir)  # 解压缩文件
