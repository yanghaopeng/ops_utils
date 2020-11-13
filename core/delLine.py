
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/29 15:06
# @Author  : hyang
# @File    : delLine.py
# @Software: 删除文件中一行

import sys
import os
import random
import shutil
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
            print_error(r"------执行%s输入参数为--------" % val)
        else:
            print_info(val)


def getLine_num(filename):
    """
    得到文件行数
    :param filename:
    :return:
    """
    count = 0
    for index, line in enumerate(open(filename, 'rb')):
        count += 1
    return count


def remove_Line(filename, del_line):
    """
    删除文件某一行
    :param filename:
    :param del_line:
    :return:
    """
    # 打开旧文件
    old_file = open(filename, "rb")
    # 打开新文件
    new_file = open("%s.new" % filename, "wb")

    current_line = 0
    # 定位到需要删除的行
    while current_line < (del_line - 1):
        current_line_cont = old_file.readline()
        # 把每一行写入新文件
        new_file.write(current_line_cont)
        current_line += 1

    # 当前光标在被删除行的行首，记录该位置
    seek_point = old_file.tell()

    # 设置光标位置
    new_file.seek(seek_point, 0)

    # 读需要删除的行，光标移到下一行行首
    line_con = old_file.readline()
    print_info("需要删除行: {}".format(line_con))

    # 被删除行的下一行读给 next_line
    next_line = old_file.readline()

    # 连续覆盖剩余行，后面所有行上移一行
    while next_line:
        new_file.write(next_line)
        next_line = old_file.readline()

    # 文件关闭
    old_file.close()
    new_file.close()

    # 文件备份与替换
    bak_f = filename + ''.join(random.sample(string.digits, 6))
    os.rename(filename, bak_f)  # 备份旧文件
    print_info("源文件备份为%s" % bak_f)
    os.rename("%s.new" % filename, filename)  # 把新文件名字改成原文件的名字，就把之前的覆盖掉了


def main_arg(v_arg):
    """
    参数处理
    :param v_arg:
    :return:
    """
    if len(v_arg) != 3:
        # print(platform.system())
        print_arg(v_arg)
        print_error("---参数输入错误--")
        print_error("delLine 文件名 删除行")
    else:
        f_name = v_arg[1].strip()
        line_no = v_arg[2].strip()  # 删除行
        if not line_no.isdigit():
            print_error("行数必须为数字" )
        else:
            if not os.path.exists(f_name):
                print_error("%s文件不存在" % f_name)
            else:
                main(f_name, line_no)


def main(f_name,line_no):
    """
    主函数
    :param f_name:
    :param line_no:
    :return:
    """
    # f_name = 'F:\home/tscmsapp/ff/logs'
    bak_f = f_name + ''.join(random.sample(string.digits, 6))
    # line_no = '2'
    line_no = int(line_no)

    line_num = getLine_num(f_name)  # 获得文件总行数
    if line_no > line_num:
        print_error("输入行数{}大于文件行数 {}".format(line_no,line_num))
    else:
        print("文件总行数={},删除第{}行" .format(line_num, line_no))
        remove_Line(f_name, line_no)


if __name__ == '__main__':
    # 获得系统参数
    v_arg = sys.argv
    main_arg(v_arg)
    # init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    # main()
    # print_color(Style.RESET_ALL)  # 还原默认颜色
