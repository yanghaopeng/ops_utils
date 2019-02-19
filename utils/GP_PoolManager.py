#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 11:00
# @Author  : hyang
# @File    : GP_PoolManager.py
# @Software: PyCharm

import os
import sys

from psycopg2.pool import ThreadedConnectionPool,PoolError
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # 加入环境变量

from conf import settings
from utils import my_logset


class GP_PoolManager:
    """
    GP 多线程连接池
    thread:ThreadedConnectionPool
    """

    def __init__(self, minconn=5, maxconn=20,
                 *args, **kwargs):
        self.db_log = my_logset.get_mylogger("gpdb_access", 'gpdb.log')
        self.last_seen_process_id = os.getpid()
        self.args = args
        self.conn_kwargs = settings.gp_db  # gp连接串
        self.minconn = minconn  # 最少连接数
        self.maxconn = maxconn  # 最多连接数

    def init_conn(self):
        """
        # Establishes the connection with the backend databases.
        :return:
        """
        try:
            self._pool = ThreadedConnectionPool(
                self.minconn, self.maxconn, *self.args, **self.conn_kwargs)
            self.db_log.info("SUCCESS: create GP Thread ConnectPool success.\n")
        except PoolError as e:
            self._pool = None
            self.db_log.error("FAIL: create GP Thread ConnectPool fail.\n")
        except Exception as e:
            raise e

    def get_conn(self):
        current_pid = os.getpid()
        if not (current_pid == self.last_seen_process_id):
            self.init_conn()
            self.db_log.info("New id is %s, old id was %s" %
                  (current_pid, self.last_seen_process_id))
            self.last_seen_process_id = current_pid
        return self._pool.getconn()

    def close_conn(self, conn):
        return self._pool.putconn(conn, close=True)
