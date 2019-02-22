#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 16:51
# @Author  : hyang
# @File    : gp_test.py
# @Software: PyCharm


import psycopg2
import psycopg2.extras
import psycopg2.pool
from datetime import datetime
from utils.GP_utils import GP_dbutils

'''
    连接数据库
    使用数据库连接池
    returns:db
'''
def gp_connect():
    try:
        simple_conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=5,dbname="testdb",
                              user="gpadmin",
                              password="gpadmin",
                              host="10.1.208.42",
                              port="5432")
        # connect()也可以使用一个大的字符串参数,
        # 比如”host=localhost port=5432 user=postgres password=postgres dbname=test”
        # 从数据库连接池获取连接
        conn = simple_conn_pool.getconn()
        return conn
    except psycopg2.DatabaseError as e:
        print("could not connect to Greenplum server",e)


if __name__ == '__main__':
    gpdb = GP_dbutils()

    print(gpdb.conn)

    # 批量查询大小
    batch_size = 1000
    # gp_uplist = []
    # for i in range(20, 10000000):
    #     gp_uplist.append((i,'def%s'%i))
    # print(gp_uplist)

    # 开始时间
    start_time = datetime.now()
    # 批量提交数据execute_values性能大于executemany
    #
    sql ="INSERT INTO public.gp_test (num, data) VALUES %s"
    # # sql = "UPDATE public.gp_test SET data = TEST.data  " \
    # #       "FROM (VALUES %s) AS TEST(num, data) " \
    # #       "WHERE  public.gp_test.num = TEST.num"
    # # 批量更新语句模版 UPDATE TABLE SET TABLE.COL = XX.col
    # # FROM (VALUES %s) AS XX(id_col,col)
    # # WHERE TABLE.id_col = XX.id_col
    # # XX为别名
    # count = gpdb.execute_bulk_update(sql,  [(i, 'def%s'%i) for i in range(20, 6000000)])
    # print(count)
    data = gpdb.execute_bulk_query("select * from gp_test ")
    # print(data[-1])
    # count = 0
    #
    # while True:
    #     count = count + 1
    #     # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
    #     data = cur.fetchmany(batch_size)
    #     # 数据为空的时候中断循环
    #     if not data:
    #         break
    #     else:
    #         print(data[-1])  # 得到最后一条(通过元祖方式返回)
    #     print('获取%s到%s数据成功' % ((count - 1) * batch_size, count * batch_size))
    # print('update到fetchmany获取全量数据所用时间:', (datetime.now() - start_time).seconds) # 16s


    # store_to('table_name', 'D:\python_file\excel2gp\\test.xlsx')
    # cur.execute("select * from pg_tables where tablename = %s", ('psy_test',))
    # psy_obj = cur.fetchone()
    # print(psy_obj)
    # cur.execute("select num, data from  tscmsdata.psy_test")
    # cur.execute("select string_agg(a.attname,',' order by attnum ) tab_cols"
    #             " from pg_attribute a join pg_class b on a.attrelid=b.oid "
    #             " where b.relname='psy_test' and a.attnum>0 and not a.attisdropped  group by attrelid")
    #
    # names = ['num', 'data']
    # psy_rows = [dict(zip(names, row)) for row in cur.fetchall()]
    # print(psy_rows)
    #
    #         # sys_time = time.ctime()
    # # print(sys_time)
# '''
#     读取excel函数
#     args：excel_file（excel文件，目录在py文件同目录）
#     returns：book
# '''
#
#
# def open_excel(excel_file):
#     try:
#         book = xlrd.open_workbook(excel_file)  # 文件名，把文件与py文件放在同一目录下
#         print(sys.getsizeof(book))
#         return book
#     except:
#         print("open excel file failed!")
#
#
# '''
#     执行插入操作
#     args:db_name（数据库名称）
#          table_name(表名称）
#          excel_file（excel文件名，把文件与py文件放在同一目录下）
# '''
#
#
# # db = gp_link(db_name)  # 打开数据库连接
# def store_to(table_name, excel_file):
#     db = gp_connect()
#     cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
#
#     book = open_excel(excel_file)  # 打开excel文件
#     sheets = book.sheet_names()  # 获取所有sheet表名
#     for sheet in sheets:
#         sh = book.sheet_by_name(sheet)  # 打开每一张表
#         row_num = sh.nrows
#         print(row_num)
#         list = []  # 定义列表用来存放数据
#         num = 0  # 用来控制每次插入的数量
#         for i in range(1, row_num):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1
#             row_data = sh.row_values(i)  # 按行获取excel的值
#             value = (row_data[0], row_data[1], row_data[2], row_data[3])
#             list.append(value)  # 将数据暂存在列表
#             print(list)
#             num += 1
#             if (num >= 10000):  # 每一万条数据执行一次插入
#                 # print(sys.getsizeof(list))
#                 sql_tru = "TRUNCATE TABLE " + table_name
#                 sql = "INSERT INTO " + table_name + " (area, 团队, name, 职级)  VALUES(%s,%s,%s,%s)"
#                 print(sql_tru)
#                 print(sql)
#                 cursor.executemany(sql, list)  # 执行sql语句
#
#                 num = 0  # 计数归零
#                 list.clear()  # 清空list
#                 print("worksheets: " + sheet + " has been inserted 1 datas!")
#
#     print("worksheets: " + sheet + " has been inserted " + str(row_num) + " datas!")
#     db.commit()  # 提交
#     db.close()  # 关闭连接
#     db.close()


