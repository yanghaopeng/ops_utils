#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/22 13:17
# @Author  : hyang
# @File    : oracle_utils.py
# @Software: PyCharm

import os
import sys
# 用于以清晰、可读的形式输出 Python 数据结构
from sys import modules

import cx_Oracle
from DBUtils.PooledDB import PooledDB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量

from conf import settings
from utils import my_logset
from utils.time_utils import run_time

"""
通过PooledDB连接Oracle，并完成常用一些操作
"""


class Ora_util(object):

    __pool = None  # 连接池对象
    _db_info = settings.prod_db

    def __init__(self, db_info=_db_info, arraysize=500):
        # 日志
        self.db_log = my_logset.get_mylogger("oradb_access", 'db.log')
        self.db_info = db_info
        self.conn = Ora_util.__getConn(db_info)
        self.cursor = self.conn.cursor()
        # 每次从数据库向Python的缓存返回arraysize=100条记录
        # self.db_log.debug('数据库已连接' )
        self.cursor.arraysize = arraysize

    @staticmethod
    def __getConn(db_info):
        # 静态方法，从连接池中取出连接
        if Ora_util.__pool is None:
            try:
                __pool = PooledDB(cx_Oracle,
                                  user=db_info['DB_USER'],
                                  password=db_info['DB_PASSWORD'],
                                  dsn=db_info['DB_SID'],
                                  mincached=20,
                                  maxcached=60)
                return __pool.connection()
            except Exception as e:
                raise 'oracle_db connect error'

    def getCurrentDate(self):
        """Return the current date according to the database."""
        cursor = self.cursor()
        cursor.execute("select sysdate from dual")
        value, = cursor.fetchone()
        return value

    def blob(self, _value):
        """Return a BLOB variable containing the given value."""
        var = self.var(self.connection.BLOB)
        var.setvalue(0, _value)
        return var

    def clob(self, _value):
        """Return a CLOB variable containing the given value."""
        var = self.var(self.connection.CLOB)
        var.setvalue(0, _value)
        return var

    def get_columns(self, table):
        # 查询表的所有列
        sql = ["select lower(column_name) column_name \
        from user_tab_columns where table_name=upper('%(table)s')"]
        rows = self.queryBySql(''.join(sql) % locals())
        col_list = [k["column_name"] for k in rows]
        # ['sjhm', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'status']

        return col_list

    # 根据表自动创建参数字典
    def create_params(self, table, args={}):
        col_list = self.get_columns(table)
        params = {}
        for k in col_list:
            if args.__contains__(k):
                params[k] = args[k]
        return params

    # 执行sql
    @run_time
    def execute(self, sql, args={}):
        try:
            self.db_log.debug('execute sql: {}'.format(sql))
            return self.cursor.execute(sql, args)
        except Exception as e:
            self.close()
            raise e

    # 调用函数 函数名，返回类型, 参数('1',2)元祖类型
    @run_time
    def callfunc(self, func, ret_type=cx_Oracle.NUMBER, args=()):
        try:
            self.db_log.debug('call func:{} {}'.format(func, args))
            return self.cursor.callfunc(func, ret_type, args)
        except Exception as e:
            self.close()
            raise e

    # 调用过程 过程名，输入参数('1',2)元祖类型
    @run_time
    def callproc(self, proc, in_val=()):
        try:
            self.db_log.debug('call proc:{} {}'.format(proc, in_val))
            return self.cursor.callproc(proc, in_val)
        except Exception as e:
            self.close()
            raise e

    # 解析sql
    def parse(self, sql, args={}):
        try:
            # 解析sql语句
            return self.cursor.parse(sql, args)
            # 捕获SQL异常
        except Exception as e:
            self.close()
            raise e

    # 批量执行
    @run_time
    def executemany(self, sql, args):
        try:
            self.db_log.debug('executemany sql:{}'.format(sql))
            return self.cursor.executemany(sql, args)
        except Exception as e:
            self.close()
            raise e

    # 执行sql，参数一：table，参数二：查询列'col1,col2' 参数三：参数字典{'字段1'：'值1','字段2':'值2'}
    def queryByTable(self, table, column='*', cond_dict={}):
        # self.execute(sql, args)
        cond_dict = self.create_params(table, cond_dict)
        cond_stmt = ' and '.join(['%s=:%s' % (k, k) for k in cond_dict.keys()])
        # del_sql = 'DELETE FROM %(table)s where %(cond_stmt)s'
        if not cond_dict:
            query_sql = 'select %(column)s FROM %(table)s'
        else:
            query_sql = 'select %(column)s FROM %(table)s where %(cond_stmt)s'

        self.execute(query_sql % locals(), cond_dict)
        return self.get_rows()

        # 执行sql，参数一：sql语句，如select * from python_modules where module_name=:module_name
        # 参数二：参数字典{'字段1'：'值1','字段2':'值2'} 如{module_name:Oracle}
    def queryBySql(self, sql, args={}):
        self.execute(sql, args)
        return self.get_rows()

    # 导出结果为文件
    def exportTxt(self, file_name, sql, args={}, col_split='|', col_flg=True, row_Limit=-1):
        """
        :param file_name: 文件位置
        :param sql:  sql语句 如select module_name,china_name from python_modules where module_name=:module_name
        :param args:  参数 如{'module_name':'oracle'}
        :param col_split: 列分隔符
        :param col_flg: 是否输出列名字段col1|col2
        :param row_Limit 设置导出行数，如果row_Limit>0 and 如果row_Limit< rows导出row_Limit行，否则导出所有行
        :return:
        """
        rt = self.queryBySql(sql, args)
        if rt:
            row_count = 0
            with open(file_name, 'w', encoding="utf-8") as fd:
                for row in rt:
                    col_info = col_split.join(row.keys())
                    val_info = ''
                    if col_flg:
                        fd.write(col_info+"\n")
                        col_flg = False
                    val_info += col_split.join(row.values())
                    val_info += '\n'
                    fd.write(val_info)
                    row_count += 1
                    if row_count == row_Limit:
                        break
            print('export data rows %s'%row_count)

    # 分页查询，参数一：sql语句，参数二：参数字典{'字段1'：'值1','字段2':'值2'}，参数三：页码，参数四：分页大小
    def query_pages(self, sql, args={}, page=1, page_size=30):
        _args, count_args = args, args
        page = int(page)
        # print "page:%s" %(page,)
        # 下一页
        next_page = page_size * page
        # 当前页
        cur_page = page_size * (page - 1)
        if page == 1 or cur_page < 0:
            cur_page = 0
            next_page = page_size
        sql = """SELECT * FROM(
            SELECT ROWNUM RN,T.* FROM(""" + sql + """)T 
            WHERE ROWNUM<=:next_page
            )WHERE RN >=:cur_page """
        count_sql = """
            SELECT COUNT(1)CNT FROM (""" + sql + """)"""
        _args["cur_page"] = cur_page
        _args["next_page"] = next_page
        rows = self.queryBySql(sql, _args)
        countrows = self.queryBySql(count_sql, count_args)
        return rows, countrows[0]['cnt']

    # oracle的参数名必须使用:代替，如 userid = :userid
    def insertOne(self, table, column_dict):
        column_dict = self.create_params(table, column_dict)
        keys = ','.join(column_dict.keys())
        values = column_dict.values()
        placeholder = ','.join([':%s' % (v) for v in column_dict.keys()])
        ins_sql = 'INSERT INTO %(table)s (%(keys)s) VALUES (%(placeholder)s)'
        # print(ins_sql % locals())
        self.execute(ins_sql % locals(), column_dict)

    # 获取序列的下一个值，传入sequence的名称
    def nextval(self, seq):
        self.cursor.execute("SELECT %(seq)s.nextval from dual " % locals())
        result = self.cursor.fetchall()
        return result[0][0]

    # 批量插入数据库，参数一：表名，参数二：['字段1','字段2',...],参数二：[('值1','值2',...),('值1','值2',...)]
    def insertMany(self, table, columns=[], values=[]):
        keys = ','.join(columns)
        placeholder = ','.join([':%s' % (v) for v in columns])
        ins_sql = 'INSERT INTO %(table)s (%(keys)s) VALUES(%(placeholder)s)'
        self.executemany(ins_sql % locals(), values)
        return self.get_rows_num()

    # 更新，参数一：表名，参数二用于set 字段1=值1，字段2=值2...格式：{'字段1':'值1','字段2':'值2'},
    # 参数三：用于where条件，如 where 字段3=值3 and 字段4=值4，格式{'字段3':'值3','字段4':'值4'}
    def updateByTable(self, table, column_dict={}, cond_dict={}):
        column_dict = self.create_params(table, column_dict)
        cond_dict = self.create_params(table, cond_dict)
        set_stmt = ','.join(['%s=:%s' % (k, k) for k in column_dict.keys()])
        cond_stmt = ' and '.join(['%s=:%s' % (k, k) for k in cond_dict.keys()])
        if not cond_dict:
            upd_sql = 'UPDATE %(table)s set %(set_stmt)s'
        else:
            upd_sql = 'UPDATE %(table)s set %(set_stmt)s where %(cond_stmt)s'
        args = dict(column_dict, **cond_dict)  # 合并成1个
        self.execute(upd_sql % locals(), args)
        return self.get_rows_num()

    # 删除，参数一：表名，#参数二：用于where条件，如 where 字段3=值3 and 字段4=值4，格式{'字段3':'值3','字段4':'值4'}
    def deleteByTable(self, table, cond_dict={}):
        cond_dict = self.create_params(table, cond_dict)
        cond_stmt = ' and '.join(['%s=:%s' % (k, k) for k in cond_dict.keys()])
        # del_sql = 'DELETE FROM %(table)s where %(cond_stmt)s'
        if not cond_dict:
            del_sql = 'DELETE FROM %(table)s'
        else:
            del_sql = 'DELETE FROM %(table)s where %(cond_stmt)s'
        self.execute(del_sql % locals(), cond_dict)
        return self.get_rows_num()

    # 提取数据，参数一提取的记录数，参数二，是否以字典方式提取。为true时返回：{'字段1':'值1','字段2':'值2'}
    def get_rows(self, size=None, is_dict=True):
        if size is None:
            rows = self.cursor.fetchall()
        else:
            rows = self.cursor.fetchmany(size)
        if rows is None:
            rows = []
        if is_dict:
            dict_rows = []
            dict_keys = [r[0].lower() for r in self.cursor.description]
            for row in rows:
                dict_rows.append(dict(zip(dict_keys, row)))
            rows = dict_rows
        return rows

    # 获取更改记录数
    def get_rows_num(self):
        return self.cursor.rowcount

    # 提交
    def commit(self):
        self.conn.commit()

    # 回滚
    def rollback(self):
        self.conn.rollback()

    # 销毁
    def __del__(self):
        self.close()

    # 关闭连接
    def close(self):
        # self.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':

    ora = Ora_util()
    create_table = """
    CREATE TABLE python_modules (
    module_name VARCHAR2(50) NOT NULL,
    file_path VARCHAR2(300) NOT NULL,
    china_name VARCHAR2(300) NOT NULL
    )
    """
    # 执行创建表
    create_flag = ora.execute(create_table)

    # 得到表所有列
    print(ora.get_columns('python_modules'))

    # 添加模块信息
    M = []
    for m_name, m_info in modules.items():
        try:
            M.append((m_name, m_info.__file__, '中国'))
        except AttributeError:
            pass

    print(len(M))

    print(ora.insertMany('python_modules',['module_name', 'file_path','china_name'],M))
    ora.commit()

    print(ora.queryBySql(sql="select * from python_modules where module_name=:module_name", args={'module_name':'DBUtils.PooledDB'}))

    print(ora.updateByTable(table='python_modules',column_dict={'china_name':'北京'},cond_dict={'module_name':'DBUtils.PooledDB'}))
    ora.commit()

    print(ora.queryBySql(sql="select * from python_modules where module_name=:module_name", args={'module_name':'DBUtils.PooledDB'}))

    print(ora.deleteByTable(table='python_modules', cond_dict={'module_name': 'DBUtils.PooledDB'}))
    ora.commit()

    print(ora.queryBySql(sql="select module_name,china_name from python_modules where module_name=:module_name", args={'module_name':'DBUtils.PooledDB'}))

    ora.updateByTable(table='python_modules', column_dict={'china_name': '河北'})
    ora.commit()
    ora.exportTxt("a.txt", sql="select * from python_modules")

    print(ora.deleteByTable(table='python_modules'))
    ora.commit()
    print(ora.queryByTable(table="python_modules"))

    ora.execute("DROP TABLE python_modules PURGE")

    print(ora.callfunc('myfunc', cx_Oracle.NUMBER, ('abc', 2)))

    print(ora.callproc('myproc',  (3,)))

    print(ora.queryByTable(table="ptab",column='mydata, myid',cond_dict={'myid':2}))
    # import Oracle_utils
    # print(help(Oracle_utils)) # 生成文档
