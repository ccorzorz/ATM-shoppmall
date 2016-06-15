#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
账单查询模块
"""
import sys,json,time,os,prettytable
sys.path.append('..')
from core import terminal_op,data_op,format_num,veri_code,time_cal,generate_bills
from conf.setting import *


def check_exist_bills():
    """
    判断账单文件是否存在
    :return: 账单文件列表
    """
    file_dir=os.listdir('../db') #将../db 目录下的内容生成列表形式
    bills_db_list=[]
    for item in file_dir:   #将以 bills.json 结尾的字符串添加进列表
        if item.endswith('bills.json'):
            bills_db_list.append(item)
    return bills_db_list



def inquire_bills(args):
    """
    账单查询函数
    :param args: 用户名
    :return:  None
    """
    #确认本月的账单文件名的日期字符串
    current_file_month=generate_bills.check_file_month()
    bills_db_list=check_exist_bills()
    if len(bills_db_list)==0:   #如果为空,提示用户无账单
        print('未到账单日,账单未生成!')
    else:
        dates=[]
        for item in bills_db_list:
            dates.append(item.split('_')[0])
        # print(dates)
        if current_file_month in dates:
            print('本月账单已生成:{}'.format(current_file_month))
            time.sleep(1)
            #加载账单数据,并显示用户欠款额度和消费记录
            bills_data=json.load(open('../db/{}_bil'
                                      'ls.json'.format(current_file_month),'r'))
            print('{}于{}月的账单'.center(52,'*').format(args,current_file_month))
            print('需还款金额:\033[31;1m{}(人民'
                  '币)\033[0m'.format(format_num.fn(bills_data[args][0])))
            print('消费记录'.center(52,'-'))
            row=prettytable.PrettyTable()
            row.field_names=['时间','交易方式','商家','金额','利息']
            record=bills_data.get(args)[1]
            # print(record)
            for item in record:
                for key in item:
                    row.add_row([key,item[key][0],item[key][1],
                                 item[key][2],item[key][3],])
            print(row)
            print('\033[31;1m请务必在下月10日(包括10日)之'
                  '前还款,否则会有每日0.05%利息产生!\033[0m')

        else:
            print('未到账单日,账单未生成!')
