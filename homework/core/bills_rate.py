#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
账单查询模块
"""

import sys,json,time
sys.path.append('..')
from core import terminal_op,data_op,format_num,veri_code,time_cal,\
    generate_bills,terminal_discover_bills
from conf.setting import *

def current_10th():
    """
    取当月10号的时间,并返回结构时间的数据
    :return: 结构时间的数据
    """
    current_10th_time=time_cal.get_10th_of_current_month()
    current_10th_time_stamp=time_cal.time_s_to_stamp(current_10th_time)
    return current_10th_time_stamp

def last_22nd():
    """
    取上个月22号的时间,并返回结构时间的数据
    :return: 结构时间的数据
    """
    last_22nd_time=time_cal.get_22nd_of_last_month()
    last_22nd_time_stamp=time_cal.time_s_to_stamp(last_22nd_time)
    return last_22nd_time_stamp

def inquire_rates(args):
    """
    查询账单利息函数
    :param args: 用户名
    :return: None
    """
    user_data=data_op.l_d()
    user_record=user_data[args][4]
    last_22nd_stamp=last_22nd()
    current_10th_stamp=current_10th()
    today=datetime.datetime.today()
    today_stamp=time_cal.time_s_to_stamp(today)
    if today_stamp <= current_10th_stamp:
        # 如未到10日,提醒用户利息为0
        print('未到本月10号,目前利率为0,如果已还款请飘过,如未还款,请速还款')
        time.sleep(1)
    else:
        #计算入账的总和
        income_list=[]
        for item in user_record:
            for key in item:    #判断目前时间是否在上月22日到本月10日之间
                if last_22nd_stamp<time_cal.str_to_stamp(key)<=current_10th_stamp:
                    income_list.append(item.get(key))
        income=[]
        for item in income_list:
            if '收款' in item or '还款' in item:
                income.append(item[2])
        income_amount=sum(income)
        current_file_month=generate_bills.check_file_month()
        bills_db_list=terminal_discover_bills.check_exist_bills()
        if len(bills_db_list)==0:   #判断是否存在账单文件
            print('暂无账单生成,请联系客服或者银行行长,每月22日生成账单')
            time.sleep(1)
        else:
            dates=[]
            for item in bills_db_list:
                dates.append(item.split('_')[0])
            if current_file_month in dates:
                bills_data=json.load(open('../db/{}_bil'
                                      'ls.json'.format(current_file_month),'r'))
                should_amount=bills_data[args][0]
                if income_amount>=should_amount:
                    # 判断入账的费用是否大于消费的费用总和
                    print('已全部还清,无逾期!')
                    time.sleep(1)
                else:#否则进行逾期天数和利息计算
                    out_rate=0.0005
                    print('有逾期还款,逾期利率为每日万分之五')
                    td=int(time.strftime('%Y%m%d'))
                    current_10th_time=time_cal.get_10th_of_current_month()
                    dead_line=[]
                    dead_line.extend(str(current_10th_time).split(' ')[0].split('-'))
                    dead_line=int(''.join(dead_line))
                    days=td-dead_line
                    interest=days*out_rate*bills_data.get(args)[0]
                    interest=format_num.fn(interest)
                    print('您有逾期费用产生,'
                          '逾期天数\033[31;1m{}\033[0m,逾期利率为万分之五,'
                          '截止到今天的逾期利息'
                          '为\033[31;1m{}\033[0m'.format(days,interest))
                    time.sleep(1)
            else:
                print('暂无账单生成')
