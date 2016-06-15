#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
查看用户信息模块
"""
import sys
sys.path.append('..')
from core import data_op,format_num

def view_credit(args):
    """
    查看用户信息,加载数据,并将相关数据显示至屏幕
    :param args:用户名
    :return:
    """
    user_data=data_op.l_d()
    if user_data.get(args)==None:
        print('无此用户.')
    else:
        balance=user_data[args][3]
        balance=format_num.fn(balance)
        credit=format_num.fn(user_data[args][2])
        print('您的信用额度:\033[31;1m{}\033[0m,目前可用信用额'
              '度为\033[31;1m{}\033[0m'.format(credit,balance))
