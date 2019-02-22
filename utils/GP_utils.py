#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/13 16:01
# @Author  : hyang
# @File    : GP_utils.py
# @Software: PyCharm

import os
import sys
# 用于以清晰、可读的形式输出 Python 数据结构
from sys import modules

import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor, execute_values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量

from conf import settings
from utils import my_logset
from utils.time_utils import run_time


class GP_dbutils(object):
    """
    通过psycopg2连接GP，并完成常用一些操作
    """
    __conn = None

    def __init__(self):
        self.gp_info = settings.gp_db
        self.db_log = my_logset.get_mylogger("gpdb_access", 'gpdb.log')
        self.conn = self.init_connect()

        # self.cursor = self.conn.cursor()

    def init_connect(self):
        try:
            if self.__conn is None:
                self.__conn = psycopg2.connect(dbname=self.gp_info['DB_NAME'],
                                               user=self.gp_info['DB_USER'],
                                               password=self.gp_info['DB_PASSWORD'],
                                               host=self.gp_info['HOST'],
                                               port=self.gp_info['PORT'])
                self.db_log.info("SUCCESS: create GP Connect success.\n")
            return self.__conn
        except psycopg2.DatabaseError as e:
            self.db_log.error(
                "ERROR: create GP Connect failed {0}\n".format(
                    str(e)))

    def __del__(self):
        '重写类被清除时调用的方法'
        if self.conn:
            self.conn.close()

    def commit(self):
        # 提交
        self.conn.commit()

    def rollback(self):
        # 回滚
        self.conn.rollback()

    def __enter__(self):
        """ implicity called before the first expression in a with-block """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ implicity called after the last expression within a with-block. """
        self.__del__()

        # https://infohost.nmt.edu/tcc/help/pubs/python/web/exit-method.html
        #   returning True surpresses any exceptions caused by the with block
        #   returning False implicitly raises exceptions caused by the with
        return False

    @run_time
    def execute_query(self, query: str, args: tuple = ()) -> (list, list):
        """ results are returned as a list of dicts"""
        if not self.conn:
            raise psycopg2.InterfaceError("null connection")

        rows = None
        self.db_log.debug('execute sql: {}'.format(query))
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                curs.execute(query, args)
                rows = curs.fetchall()
        except Exception as e:
            self.db_log.error(str(e))
            raise e

        if len(rows) == 0:
            return []
        return rows

    @run_time
    def execute_bulk_query(self, query: str, args: tuple = ()):
        """ results are returned as a list of dicts"""
        if not self.conn:
            raise psycopg2.InterfaceError("null connection")

        rows = None
        self.db_log.debug('execute sql: {}'.format(query))
        try:
            with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as curs:
                count = 0
                # 批量查询大小
                batch_size = 1000
                # curs.itersize = 1000000 # 设置服务端游标每次返回数目
                curs.execute(query, args)
                while True:
                    count = count + 1
                    # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
                    data = curs.fetchmany(batch_size)
                    # 数据为空的时候中断循环
                    if not data:
                        break
                    else:
                        print(data[-1])  # 得到最后一条
                    print('获取%s到%s数据成功' % ((count - 1) * batch_size, count * batch_size))
        except Exception as e:
            self.db_log.error(str(e))
            raise e

        return None


    @run_time
    def execute_update(self, sql: str, args: tuple = ()) -> int:
        """ perform a write query
        query -- the query string with optional %s placeholders
        args -- optional tuple of values for %s placeholders
        returns number of rows modified
        """
        if not self.conn:
            raise psycopg2.InterfaceError("null connection")

        self.db_log.debug('execute sql: {}'.format(sql))
        try:
            with self.conn.cursor() as curs:
                curs.execute(sql, args)
        except Exception as e:
            self.db_log.error(str(e))
            raise e

        return curs.rowcount

    @run_time
    def execute_bulk_update(self, sql: str, args_list: list = []) -> int:
        """ perform a bulk update
        query -- the sql string with optional %s placeholders
        args -- optional list of values for %s placeholders
        returns number of rows modified
        """
        if not self.conn:
            raise psycopg2.InterfaceError("null connection")

        self.db_log.debug('execute sql: {}'.format(sql))
        try:
            with self.conn.cursor() as curs:
                psycopg2.extras.execute_values(
                    curs, sql, args_list, page_size=1000)
                self.commit()
            return len(args_list)
        except Exception as e:
            self.rollback()
            self.db_log.error(str(e))
            raise e

    def generate_query(self, query: str, args: tuple = ()) -> str:
        """ return the query string, with the given parameters, that would be executed against the database.
        nothing is executed.
        """
        if not self.conn:
            raise psycopg2.InterfaceError("null connection")

        try:
            with self.conn.cursor() as curs:
                query_string = curs.mogrify(query, args)
        except Exception as e:
            self.db_log.error(str(e))
            raise e

        return query_string.decode("utf-8")
