#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 14:50
# @Author  : hyang
# @File    : psutil_demo.py
# @Software: PyCharm

import os
import socket
from datetime import datetime
import psutil

import jinja2
import yagmail



EMAIL_USER = 'joy_lmx@163.com'
EMAIL_PASSWORD = '123456'
RECIPIENTS = ['me@mingxinglai.com']


def render(tpl_path, **kwargs):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(**kwargs)


def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        # << 左移” 左移一位表示乘2 即1 << 1=2，二位就表示4 即1 << 2=4，
        # 10位就表示1024 即1 << 10=1024 就是2的n次方
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def get_cpu_info():
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    return dict(cpu_count=cpu_count, cpu_percent=cpu_percent)


def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    print(virtual_mem)
    mem_total = bytes2human(virtual_mem.total)
    mem_percent = virtual_mem.percent
    mem_free = bytes2human(virtual_mem.free + virtual_mem.buffers + virtual_mem.cached)
    mem_used = bytes2human(virtual_mem.total * virtual_mem.percent)

    return dict(mem_total=mem_total, mem_percent=mem_percent,
                mem_free=mem_free, mem_used=mem_used)


def get_disk_info():
    disk_usage = psutil.disk_usage('/')

    disk_total = bytes2human(disk_usage.total)
    disk_percent = disk_usage.percent
    disk_free = bytes2human(disk_usage.free)
    disk_used = bytes2human(disk_usage.used)

    return dict(disk_total=disk_total, disk_percent=disk_percent,
                disk_free=disk_free, disk_used=disk_used)


def get_boot_info():
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    return dict(boot_time=boot_time)


def collect_monitor_data():
    data = {}
    data.update(get_boot_info())
    data.update(get_cpu_info())
    data.update(get_memory_info())
    data.update(get_disk_info())
    return data


def main():

    hostname = socket.gethostname()
    data = collect_monitor_data()
    data.update(dict(hostname=hostname))
    print(data)

    # content = render('monitor.html', **data)
    # print content
    #
    # with yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASSWORD,
    #                   host='smtp.163.com', port=25) as yag:
    #     for recipient in RECIPIENTS:
    #         yag.send(recipient, "监控信息".encode('utf-8'), content.encode('utf-8'))


if __name__ == '__main__':
    main()
