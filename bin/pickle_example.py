#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 9:28
# @Author  : hyang
# @File    : pickle_example.py
# @Software: PyCharm


import pickle
class MyPickle():

    def __init__(self,file_name):
        self.file_name = file_name

    def dump(self,obj):
        """
        序列化对象
        :param obj:
        :return:
        """
        with open(self.file_name,'ab') as f:
            pickle.dump(obj, f)
            print('dump data',obj.__dict__)

    def loaditer(self):
        """
        迭代反序列化对象
        :return:
        """
        f = open(self.file_name, 'rb')
        while True:
            try:
                obj = pickle.load(f)
                yield obj
            except EOFError:
                print('EOFError')
                f.close()
                print(f.closed)
                break

class Person:
    def __init__(self,n,a):
        self.name=n
        self.age=a
    def show(self):
        print(self.name+"_"+str(self.age) )

aa = Person("aGood", 2)
bb = Person("bGood",3)
cc = Person("cGood",4)

p = MyPickle('c.txt')
p.dump(aa)
p.dump(bb)
p.dump(cc)

iter_obj = p.loaditer()
while True:
    try:
        # print(next(iter_obj).__dict__)
        next(iter_obj).show()
    except StopIteration:
        print('stop')
        break

