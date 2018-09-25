#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 15:46
# @Author  : hyang
# @File    : py_queryTest.py
# @Software: PyCharm
from pyquery import PyQuery as pq

html = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap')
print(wrap.text())
wrap.find('p').remove()
print(wrap.text())