# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# # @Time    : 2018/7/4 19:12
# # @Author  : hyang
# # @File    : copy_test.py
# # @Software: PyCharm
#
# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# # Date: 2018/7/1
#
# import os
# import time
# import gevent
# import shutil
# import threading
#
# from functools import wraps
#
# from concurrent import futures
#
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
#
# # from concurrent.futures import ThreadPoolExecutor
# # from concurrent.futures import ProcessPoolExecutor
#
#
# def timer(func_type):
#     def run_time(func):
#         """
#         计算程序运行时间的装饰器
#         """
#
#         @wraps(func)
#         def decor(*args, **kwargs):
#             start = time.time()
#             res = func(*args, **kwargs)
#             end = time.time()
#             print("使用 {:6} 拷贝文件运行时间: {:.4f}s ".format(func_type, end - start))
#             return res
#
#         return decor
#     return run_time
#
#
# def copy_file(from_file_path, to_file_path):
#
#     shutil.copy(from_file_path, to_file_path)  # copy file
#
#
# @timer("单线程")
# def upload1(from_path, to_path):
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             dst_file_path = os.path.abspath(
#                 local_file_path.replace(
#                     from_path, to_path))  # 目标文件路径 如/dst/q.txt
#             dst_dir = os.path.dirname(dst_file_path)  # 目标文件路径文件夹 如/dst/
#             if not os.path.isdir(dst_dir):
#                 os.makedirs(dst_dir)  # 创建目录
#
#             copy_file(local_file_path, dst_file_path)  # copy file
#
#
# @timer("多线程1")
# def upload2_0(from_path, to_path):
#     """
#
#     """
#     pool = ThreadPool(3)
#
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             dst_file_path = os.path.abspath(
#                 local_file_path.replace(
#                     from_path, to_path))  # 目标文件路径 如/dst/q.txt
#             dst_dir = os.path.dirname(dst_file_path)  # 目标文件路径文件夹 如/dst/
#             if not os.path.isdir(dst_dir):
#                 os.makedirs(dst_dir)  # 创建目录
#
#             pool.apply_async(copy_file, args=(local_file_path, dst_file_path), kwds={})
#
#     # pool.close()
#     # pool.join()
#
#
# @timer("多线程2")
# def upload2_1(from_path, to_path):
#
#     task_list = []
#
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             to_file_path = os.path.abspath(os.path.join(to_path, file))  # 目标
#             task = threading.Thread(
#                 target=copy_file,
#                 args=(local_file_path, to_file_path, ),
#             )
#             task_list.append(task)
#             task.start()
#
#     # 注释与否速度也会发生变化的
#     # for task in task_list:
#     #     task.join()
#
#
# @timer("多线程3")
# def upload2_2(from_path, to_path):
#
#     with futures.ThreadPoolExecutor(max_workers=3) as executor:
#
#         for root, dirs, files in os.walk(from_path):
#
#             future_tasks = dict(
#                 (executor.submit(
#                     copy_file,
#                     os.path.join(root, file),
#                     os.path.abspath(os.path.join(to_path, file))
#                 ),
#                 file
#                 ) for file in files
#             )
#
#             for future in futures.as_completed(future_tasks):
#                 if future.exception() is not None:
#                     print("error")
#
#
# @timer("多进程1")
# def upload3_0(from_path, to_path):
#
#     pool = Pool(3)
#
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             to_file_path = os.path.abspath(os.path.join(to_path, file))  # 目标
#             pool.apply_async(copy_file, [local_file_path, to_file_path])
#
#     # pool.close()
#     # pool.join()
#
#
# @timer("多进程2")
# def upload3_1(from_path, to_path):
#
#     task_list = []
#
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             to_file_path = os.path.abspath(os.path.join(to_path, file))  # 目标
#
#             task = Process(
#                 target=copy_file,
#                 args=(local_file_path, to_file_path,)
#             )
#             task_list.append(task)
#             task.start()
#
#     # for task in task_list:
#     #     task.join()
#
#
# @timer("协程")
# def upload4(from_path, to_path):
#
#     task_list = []
#
#     for root, dirs, files in os.walk(from_path):
#
#         for file in files:
#
#             local_file_path = os.path.join(root, file)
#             to_file_path = os.path.abspath(os.path.join(to_path, file))  # 目标
#             task_list.append(gevent.spawn(
#                 copy_file,
#                 local_file_path,
#                 to_file_path
#             ))
#
#     gevent.joinall(task_list)
#
#
# if __name__ == '__main__':
#     upload1(
#         "D:\copytest2",
#         "D:\copyfile1"
#     )
#
#     upload2_0(
#         "D:\copytest2",
#         "D:\copyfile2"
#     )
#
#     # upload2_1(
#     #     "d:/MongoDB",
#     #     "d:/copyfile3"
#     # )
#     #
#     # upload2_2(
#     #     "d:/MongoDB",
#     #     "d:/copyfile4"
#     # )
#     #
#     # upload3_0(
#     #     "d:/MongoDB",
#     #     "d:/copyfile5/"
#     # )
#     #
#     # upload3_1(
#     #     "d:/MongoDB",
#     #     "d:/copyfile6/"
#     # )
#     #
#     # upload4(
#     #     "d:/MongoDB",
#     #     "d:/copyfile7"
#     # )

import time, threading

# 新线程执行的代码:
def loop(x):
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 3:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

if __name__ == '__main__':

    print('thread %s is running...' % threading.current_thread().name)
    pool = ThreadPool(3)
    pool.apply_async(loop, kwds={})
    for i in range(3):
        msg = "hello %d" % (i)
        # result.append(pool.apply_async(func, (msg,)))
    # result = []
    # result.append(pool.apply_async(loop, kwds={}))
    # for res in result:
    #     print(":::",res.get())
    pool.close()
    pool.join()
    print('thread %s ended.' % threading.current_thread().name)
