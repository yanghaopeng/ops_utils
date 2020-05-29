#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 14:50
# @Author  : hyang
# @File    : fileRead.py
# @Software: PyCharm


import sys
import os
import random
import string
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量
from utils.print_log import print_info, print_warn, print_error


def print_arg(arg):
    """
    打印参数
    :param arg:
    :return:
    """

    for ind, val in enumerate(arg):
        if ind == 0:
            print_warn(r"------执行%s输入参数为--------" % val)
        else:
            print_info(val, end=",")


def print_color(color, mes=""):
    """
     打印颜色+字符
    :param color:
    :param mes:
    :return:
    """
    print(color + mes)


def main():
    """
    字符替换
    :return:
    """
    if len(v_arg) != 4:
        # print(platform.system())
        print_arg(v_arg)
        print_warn("---参数输入错误--")
        print_warn("fileRead.py 文件名 列数")
    else:
        f_name = v_arg[1].strip()
        input_len = v_arg[2].strip()

        # old_str = v_arg[2].strip()  # 旧字符
        # new_str = v_arg[3].strip()  # 替换的新字符
        f_new_name = "%s.new" % f_name
        count = 0  # 新文件行数
        if not os.path.exists(f_name):
            print_error("%s文件不存在" % f_name)
        else:
            f_new = open(f_new_name, 'w')
            f = open(f_name, "r", )
            for line in f:  # 读取大文件
                length = len(line.split(r"|"))

                if(input_len != length):
                    new_line = line
                    count += 1
                    f_new.write(new_line)  # 内容写新文件

            f.close()
            f_new.close()

            if count == 0:
                print_warn("文件列数符合标准")
            else:
                # bak_f = f_name + ''.join(random.sample(string.digits, 6))
                # os.rename(f_name, bak_f)  # 备份旧文件
                # os.rename(f_new_name, f_name)  # 把新文件名字改成原文件的名字，就把之前的覆盖掉了
                print_warn("文件[{}]列数不符合标准".format(f_name))
                print_info("文件生成成功,共%s行，文件名[%s]" % (count, f_new_name))


if __name__ == '__main__':
    # 获得系统参数
    v_arg = sys.argv
    # init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    main()
    # print_color(Style.RESET_ALL)  # 还原默认颜色
