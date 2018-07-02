#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/30 15:30
# @Author  : hyang
# @File    : preety_table_test.py
# @Software: PyCharm

import os
import sys
from sys import modules
from prettytable import PrettyTable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量

from utils.oracle_utils import Ora_util


if __name__ == '__main__':

    ora = Ora_util()
    ora.execute("DROP TABLE python_modules PURGE")
    create_table = """
        CREATE TABLE python_modules (
        module_name VARCHAR2(50) NOT NULL,
        file_path VARCHAR2(300) NOT NULL,
        t_id INT NOT NULL
        )
        """
    # 执行创建表
    create_flag = ora.execute(create_table)

    # 得到表所有列
    print(ora.get_columns('python_modules'))

    # 添加模块信息
    M = []
    count = 1
    for m_name, m_info in modules.items():
        try:
            M.append((m_name, m_info.__file__, count))
            count += 1
        except AttributeError:
            pass

    print(len(M))

    print(ora.insertMany('python_modules',['module_name', 'file_path','t_id'],M))
    ora.commit()

    from prettytable import from_db_cursor

    tb = from_db_cursor(ora.execute('select * from python_modules'))
    ### 设定左对齐
    tb.align = 'l'
    ### 设定T_ID右对齐
    tb.align["T_ID"]="r"
    ### 设定数字输出格式
    tb.float_format = "2.2"
    ### 设定边框连接符为'*"
    tb.junction_char = "*"
    ### 设定排序列
    tb.sortby = "T_ID"
    ### 设定排序方式
    tb.reversesort = True
    ### 设定左侧不填充空白字符
    tb.left_padding_width = 0

    # print(tb)
    # with open('1.txt','a+') as f:
    #     f.write(pt.get_string())
    # res_dict = ora.queryByTable(table="python_modules")
    # # print(res_dict)
    # if res_dict:
    #     table = PrettyTable(res_dict[0].keys())
    #     table.padding_width = 1   # 填充宽度
    #     # table.sort_key("china_name")
    #     # table.reversesort = False
    #     for item in res_dict:
    #         table.add_row(item.values())
    #         # print(item.values())
    #     # print(table.get_string())
    #     # from prettytable import MSWORD_FRIENDLY
    #     # table.set_style(MSWORD_FRIENDLY)
    #
    #     table.border = True
    #     table.header = True
    #     table.padding_width = 5
    #     table.align="l"  # 第一列左对齐
    #     table.align["t_id"] = "r"  # t_id 列右对齐
    #     # print(table.get_html_string())  # HTML表
    # print(pt.get_string(fields=[ 'file_path','t_id'])) # 选择子表
    #     # print(table.get_string(sortby="t_id", reversesort=True))


import prettytable as pt

##按行添加数据
tb = pt.PrettyTable()
tb.field_names = ["City name", "Area", "Population"]  # 字段名
tb.add_row(["A1",125, 115825.9])  # 增加行
tb.add_row(["B1",595, 1857594])
tb.add_row(["C1", 12, 120900])
tb.add_row(["D1", 135, 20555.6])

s = tb.get_string(fields=["City name", "Population"],start=0,end=3)
print(s)
# ## 自定义表格输出样式
# ### 设定左对齐
# tb.align = 'l'
# ### 设定数字输出格式
# tb.float_format = "2.2"
# ### 设定边框连接符为'*"
# tb.junction_char = "*"
# ### 设定排序列
# tb.sortby = "Population"
# ### 设定排序方式
# tb.reversesort=True
# ### 设定左侧不填充空白字符
# tb.left_padding_width = 0
#
# s = tb.get_html_string()


