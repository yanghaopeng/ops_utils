# import click
#
# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)
#
# if __name__ == '__main__':
#     hello()



# @click.group()
# def cli():
#     pass
#
# @click.command()
# def initdb():
#     click.echo('Initialized the database')
#
# @click.command()
# def dropdb():
#     click.echo('Dropped the database')
#
# cli.add_command(dropdb)
# if __name__ == '__main__':
#     cli()
# def wrapper1(func):
#     def inner():
#         print('wrapper1 ,before func')
#         func()
#         print('wrapper1 ,after func')
#     return inner
#
# def wrapper2(func):
#     def inner():
#         print('wrapper2 ,before func')
#         func()
#         print('wrapper2 ,after func')
#     return inner
#
# @wrapper2
# @wrapper1
# def f():
#     print('in f')
#
# f()
#
import time
from functools import wraps
from utils.time_utils import run_time
args={'user':1,'pwd':2}
l = ["%s = :%s" % (n, n) for n in args]
print(l)

@run_time
def add(n):
    y = 1
    x = 1
    while x <= n:
        y += x
        x += 1

    return y

print(add(50000000))


#
#
#
# f1(50)
#
# # 符合开闭原则
# # 闭包函数
# # 给原函数增加新功能，不用修改被装饰的函数代码
# # 嵌套函数中内部的函数包含了对外部作用域变量的引用，非全局变量就是闭包
#
from functools import reduce
li = [i for i in range(1,9)]
print(list(map(lambda x:x*x,li)))
def f1(x):
    if x%2 == 1:
        return True
print(list(filter(f1, li)))
print(reduce(lambda x,y:x+y,li))
a = [1,2,3]
b = ['a','b','c']
print(list(zip(b,a)))
#
# # 生成器就是迭代器
# # 实现了next()方法
# # 使用生成器节省内存，
# #  不能
# #  Iter(list)
# #  iterable
# # 生成器就是迭代器本质是流对象，没有长度，通过next（）直接
# #
# # list长度大小是固定的
# (i for i in range(1,9))


# def func(n):
#     a,b,c=0,1,0
#     while c < n:
#         print(b)
#         yield b
#         a,b = b,a+b
#         c+=1
#
#
# x = func(5)
# next(x)
# next(x)
# next(x)
# next(x)
# next(x)
# next(x)
# import time
#
# print(time.localtime())
#
# print(time.strftime('%Y-%m-%d' ,time.localtime()))
#
# # 返回str，参数列表
# # 第一个值
#
# import sys
#
#
# print(sys.argv)
# # 第一参数是代码
#
# # # 再说一遍，没有听清
# # eval()
# # exec() # ke执行多行
# # #执行python代码，
#
# # 写了
#
# # with open('README.md','r',encoding='utf-8') as f:
# #     for line in f:
# #         print(line)

li = list(range(1, 200))
# x = 'abc'
# print(x[-1：])
print(list(filter(lambda x: int(str(x)) == int(str(x)[::-1]),li)))


# 9.利用内置函数chr(),ord()以及 random模块写一个简单随机4位验证码(编程)
import random
codes = ''

for i in range(0,4):
    num = random.randint(0,9)
    uplet = chr(random.randint(ord('A'), ord('Z')))  # 大写字母
    lolet = chr(random.randint(ord('a'), ord('z')))   # 小写字母
    ran = random.choice([num, uplet, lolet])
    codes = ''.join([codes, str(ran)])

print(codes)

# 5.os()
# 请用os模块判断某个目录是否存在(例如:/user/lib/),如果有不创建该目录,反之则创建此目录
import os
import time
# path = r'C:/user/lib/'
# if not os.path.isdir(path):
#     os.makedirs(path)

# 请用os模块获取一个文件的大小,创建时间
print(os.path.getsize(__file__))
print(time.localtime(os.path.getctime(__file__)))
# 6.序列化json,xml,pickle(口述)
# json文件读取快，占用空间小，可以在不同的编程语言中中进行数据交换
# xml文件读取快，占用空间大,可以在不同的编程语言中进行数据交换(早期编程语言都用xml)
# pickle序列化只能用于python语言

# json和 pickle的区别是什么?
# json序列化只能对列表，字典，字符串，int类型,bool类型
# pickle序列化可以对所有python对象


# 简述内置函数 globals0 locals0的作用(口述)
# 1 locals()返回是当前局部变量的深拷贝,修改
# Locals()中变量值的时候,实际上对于原变量本身是没有任何影响的。
# globals()返回的是全局变量的字典,修改其中的内容,值会真正的发生改变。

# 8. logging(口述)
# logging模块写日志时如何指定写入文件编码?
# import logging
# from logging import handlers
# handlers.RotatingFileHandler(encoding='utf-8')
# logging.FileHandler(encoding='utf-8')

# 11.利用 hashlib模块和open函数写一个三次验证密码,要求如下:(编程)
# 密码是加密的。
# 三次登陆失败锁定账号在文件当中
# 登陆成功:使用一个全局变量进行记录

import hashlib
import os
import json

md5 = hashlib.md5()
# md5.update('abc'.encode('utf-8'))
# print(md5.hexdigest())
# 密码为abc
count = 0
while count < 3:
    name = input("input name > ").strip()
    pwd = input("input pwd > ").strip()
    f_name = "%s.json"%name
    # f_new_name = '%s.new'%f_name
    if os.path.exists(f_name):
        with open(f_name,'r+',encoding='utf-8') as f:
            user_d = json.load(f)
            if user_d['state'] == 0:
                md5.update(pwd.encode('utf-8'))
                encry_pwd = md5.hexdigest()
                # print(encry_pwd)

                if encry_pwd == user_d['password']:
                    print('user login success')
                    break
                else:
                    print('user login failure, password is not correct')
                    count += 1
                    if count == 3:
                        user_d['state'] = -1
                        f.seek(0)
                        f.truncate()  # 清空文件内容
                        json.dump(user_d,f,ensure_ascii=False)  # 写入文件
                        print('lock user')
            else:
                print('user is locked')
                break

    else:
        print('username is not exist!')
        break
