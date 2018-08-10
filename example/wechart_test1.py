#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 10:49
# @Author  : hyang
# @File    : wechart_test1.py
# @Software: PyCharm
import time
import requests


def crawl(offset=0):
    """
    爬取更多文章
    """
    # appmsg_token需刷新
    url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI1NjE2MTUzNg==&f=json&offset={offset}&count=10&is_ok=1&scene=124&uin=MTA1MzA1Nzk4Mw%3D%3D&key=14a4d14470b4cf90ef6c1bdfe0c0bc73c9e32bd6826385dee4f986b862669378f26e743b67ab067f5b0b7befd6d4b0099b9b16254d71f7c6e7d3ad406976f95cb477bffeb601d7d20e59603fea68ed10&pass_ticket=LG2u0K7fzmx47cbBEsGg65xkocMaK1iCadtBI2f7fb6Ak6mKao8U9aKnMiAENlRJ&wxtoken=&appmsg_token=969_yjqZ8jkiwfAFq1wJSFsCgvXQvFz6YBJpgXD9hw~~&x5=0&f=json".format(
        offset=offset)

    # 从 Fiddler 获取最新的请求头参数
    # 设置headers
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400'
    }

    # 将"Host: mp.weixin.qq.com"格式的字符串转换成字典类型转换成字典类型
    response = requests.get(url, headers=headers, verify=False)
    result = response.json()
    print(result)
    if result.get("ret") == 0:
        msg_list = result.get("general_msg_list")
        print("抓取数据：offset=%s, data=%s" % (offset, msg_list))

        # 递归调用直到 can_msg_continue 为 0 说明所有文章都爬取完了
        has_next = result.get("can_msg_continue")
        if has_next == 1:
            next_offset = result.get("next_offset")  # 下一次请求的起始位置
            time.sleep(2)
            crawl(next_offset)
    else:
        # 错误消息
        print("请求参数失效，请重新设置")
        exit()


crawl()
