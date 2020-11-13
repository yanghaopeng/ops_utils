#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/13 11:07
# @Author  : hyang
# @File    : threadtest.py
# @Software: PyCharm

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import currentThread
import os, time, random


def task(n):
    print("%s is running " % currentThread().getName())
    time.sleep(random.randint(1, 3))
    return n * 2


if __name__ == '__main__':
    start = time.time()
    executor = ThreadPoolExecutor(4)  # 线程池

    res = []
    for i in range(10):  # 开启10个任务
        future = executor.submit(task, i)  # 异步提交任务
        res.append(future)

    executor.shutdown()  # 等待所有线程执行完毕
    print("++++>")
    for r in res:
        print(r.result())  # 打印结果

    end = time.time()
    print(end - start)