#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
消费记录模块
"""
import sys,prettytable
sys.path.append('..')
from core import data_op,format_num

def show_record(args):
    """
    查看交易记录函数
    :param args: 用户名
    :return: None
    """
    user_data=data_op.l_d()
    records=user_data.get(args)[4]
    if len(records)==0:
        print('无消费记录!')
    else:
        row=prettytable.PrettyTable()
        row.field_names=['时间','交易','商家','交易金额','利息']
        for item in records:
            for record in item:
                row.add_row([record,item[record][0],item[record][1],
                             item[record][2],item[record][3]])
        print(row)
