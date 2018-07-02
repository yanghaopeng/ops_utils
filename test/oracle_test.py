#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 11:14
# @Author  : hyang
# @File    : oracle_test.py
# @Software: PyCharm


import os
import cx_Oracle
# 用于以清晰、可读的形式输出 Python 数据结构
from pprint import pprint
from sys import modules
from DBUtils.PooledDB import PooledDB

# * mincached ：启动时开启的空连接数量
# * maxcached ：连接池最大可用连接数量
# * maxshared ：连接池最大可共享连接数量
# * maxconnections ：最大允许连接数量
# * blocking ：达到最大数量时是否阻塞
# * maxusage ：单个连接最大复用次数
# * setsession ：用于传递到数据库的准备会话，如 [”set name UTF-8″] 。



# 通过客户端连接oracle
connection = cx_Oracle.connect('tscmsapptest/tscmsapptest@ORCLAPPDB')
# pool= PooledDB(cx_Oracle,user='tscmsapptest',
#                               password='tscmsapptest',dsn='ORCLAPPDB',mincached=5, maxcached=20)
# print(pool.connection())
print(connection.version)

# 获得游标对象
cursor = connection.cursor()
cursor.arraysize = 100

try:
    # 解析sql语句
    cursor.parse("select *  dual")
    # 捕获SQL异常
except cx_Oracle.DatabaseError as e:
    print(e)   # ORA-00923: 未找到要求的 FROM 关键字

# 执行sql 语句
cursor.execute ("select * from dual")
# 提取一条数据，返回一个元祖
row = cursor.fetchone()
pprint(row)  # ('X',)


create_table = """
CREATE TABLE python_modules (
module_name VARCHAR2(50) NOT NULL,
file_path VARCHAR2(300) NOT NULL,
china_name VARCHAR2(300) NOT NULL
)
"""
# 执行创建表
create_flag = cursor.execute(create_table)

# 添加模块信息
M = []
for m_name, m_info in modules.items():
    try:
        M.append((m_name, m_info.__file__,'中国'))
    except AttributeError:
        pass

print(len(M))

insert_sql = "INSERT INTO python_modules(module_name, file_path,china_name) VALUES (:1, :2, :3)"

# 在prepare之后，你再去execute的时候，就不用写上sql语句参数了
cursor.prepare(insert_sql)
cursor.executemany(None, M)  # 注意，第一个参数是None
connection.commit()  # 提交

# 查询
r = cursor.execute("SELECT COUNT(*) FROM python_modules")
pprint(cursor.fetchone())

# 查询列字段信息
column_data_types = cursor.execute('SELECT * FROM python_modules')
pprint(column_data_types.description)
# [('MODULE_NAME', <class 'cx_Oracle.STRING'>, 50, 50, None, None, 0),
#  ('FILE_PATH', <class 'cx_Oracle.STRING'>, 300, 300, None, None, 0)]

# 取10条记录信息
pprint(len(cursor.fetchmany(10)))  # 10

# 取之后所有记录信息，不包括前10条
pprint(len(cursor.fetchall()))  # 41


# 绑定变量模式查询
named_params = {'MODULE_NAME': 'cx_Oracle'}
cursor.execute('SELECT * FROM python_modules where MODULE_NAME =:MODULE_NAME',named_params)
# 在使用已命名的绑定变量时，您可以使用游标的 bindnames() 方法检查目前已指定的绑定变量：
print(cursor.bindnames())
pprint(cursor.fetchone())
# ('cx_Oracle',
#  'C:\\Program '
#  'Files\\Python36\\lib\\site-packages\\cx_Oracle.cp36-win_amd64.pyd')

# 在绑定时，您可以首先准备该语句，然后利用改变的参数执行 None。
# 根据绑定变量时准备一个语句即足够这一原则，
# Oracle 将如同在上例中一样对其进行处理。准备好的语句可执行任意次。
cursor.prepare('SELECT * FROM python_modules where MODULE_NAME =:MODULE_NAME')
cursor.execute(None, named_params)
pprint(cursor.fetchone())
# ('cx_Oracle',
#  'C:\\Program '
#  'Files\\Python36\\lib\\site-packages\\cx_Oracle.cp36-win_amd64.pyd')

# 删除python_modules
cursor.execute("DROP TABLE python_modules PURGE")

# 关闭游标
cursor.close()
# 关闭连接
connection.close ()

# BLOB & CLOB 格式的创建:
#
# binary_content = cursor.var(cx_Oracle.BLOB)
# binary_content.setvalue(0, content)