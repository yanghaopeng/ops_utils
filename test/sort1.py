#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/11 16:52
# @Author  : hyang
# @File    : sort1.py
# @Software: PyCharm



def insert_sort(lists):
    # 选择排序
    count = len(lists)
    k=0

    for i in range(1,count):
        key = lists[i]
        j=i-1
        while j >=0:
            if lists[j]>key:
                lists[j+1]=lists[j]
                lists[j]=key
                k += 1
                print("比较排序%s次序列为：" %k)
                for t in lists:
                    print(t, end=','),
            j = j-1


    return lists

if __name__ == "__main__":
    lists = [3,4,2,8,9,5,1]
    print("排序前序列为："),
    for i in lists:
        print(i,end=','),
    sort_l= insert_sort(lists)
    print("\n排序后结果为："),
    for i in sort_l:
        print(i,end=',')
