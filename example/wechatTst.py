#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 8:39
# @Author  : hyang
# @File    : wechatTst.py
# @Software: PyCharm


# coding=utf-8
from datetime import datetime
# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
import itchat
from wxpy import *
bot = Bot(cache_path=True)

# def SentChatRoomsMsg(name, context):
#     itchat.get_chatrooms(update=True)
#     iRoom = itchat.search_chatrooms(name)
#     for room in iRoom:
#         if room['NickName'] == name:
#             userName = room['UserName']
#             break
#     itchat.send_msg(context, userName)
#     print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
#         "发送到：" + name + "\n"
#         "发送内容：" + context + "\n")
#     print("*********************************************************************************")
#
# def loginCallback():
#     print("***登录成功***")
#
# def exitCallback():
#     print("***已退出***")
#
# # itchat.auto_login(hotReload=True, enableCmdQR=True, loginCallback=loginCallback, exitCallback=exitCallback)
# itchat.auto_login(loginCallback=loginCallback, exitCallback=exitCallback)
# SentChatRoomsMsg('千懿','Hello')
#
# # scheduler = BlockingScheduler()
# index = 1
# for i in range(1, iRows):
#     textList = sheet.row_values(i)
#     name = textList[0]
#     context = textList[2]
#     float_dateTime = textList[1]
#     date_value = xlrd.xldate_as_tuple(float_dateTime, workbook.datemode)
#     date_value = datetime(*date_value[:5])
#     if datetime.now() > date_value:
#         continue
#     date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
#     textList[1] = date_value
  #   scheduler.add_job(SentChatRoomsMsg, 'date', run_date=date_value,
  #   　　kwargs={"name": name, "context": context})
  #   print("任务" + str(index) + ":\n"
  #   　　"待发送时间：" + date_value + "\n"
  #  　　 "待发送到：" + name + "\n"
  # 　　  "待发送内容：" + context + "\n"
  #  　　 "******************************************************************************\n")
#     index = index + 1
#
# if index == 1:
#     print("***没有任务需要执行***")
# scheduler.start()