#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 15:07
# @Author  : hyang
# @File    : zip_util.py
# @Software: PyCharm

import zipfile
import os.path
import os


class ZFile(object):

    def __init__(self):
        pass

    def zip_file(self, fs_name, fz_name):
        """
        从压缩文件
        :param fs_name: 源文件名
        :param fz_name: 压缩后文件名
        :return:
        """
        if fs_name and fz_name:
            try:
                with zipfile.ZipFile(fz_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(fs_name)
                print('压缩文件[{}]成功'.format(fs_name))
                if not zipfile.is_zipfile(fs_name):
                    os.remove(fs_name)
                    print('删除文件[{}]成功'.format(fs_name))
            except Exception as e:
                print('压缩文件[{}]失败'.format(fs_name), str(e))
        else:
            print('文件名不能为空')


if __name__ == '__main__':
    zf = ZFile()
    # os.chdir('F:\test\data20180206\14120000\test')
    dir = 'F://test/data20180206/14110000/test/'

    if os.path.isdir(dir):  # 判断是否为目录
        os.chdir(dir)
        for file in os.listdir(
                dir):  # 遍历目录下所有文件，
            file_prefix = os.path.splitext(os.path.join(dir, file)) # 得到文件前缀和后缀名
            if len(file_prefix)>1 and 'ZIP' not in file_prefix[1]:
                zf.zip_file(file, '%s.ZIP' % os.path.splitext(os.path.join(dir, file))[0])  # 压缩文件

