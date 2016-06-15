#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
账单生成模块
"""
import sys,json,time
sys.path.append('..')
from core import terminal_op,data_op,format_num,veri_code,time_cal
from conf.setting import *
from core.logger import *

def generate_bills(args):
    """
    用户账单内容生成函数
    :param args: 用户名
    :return: 指定用户的欠款和消费记录内容
    """
    user_data=data_op.l_d()
    records=user_data.get(args)[4]
    #上月22日,本月22日的时间戳生成
    last_22=time_cal.get_22nd_of_last_month()
    last_22_stamp=time_cal.time_s_to_stamp(last_22)
    current_22=time_cal.get_22nd_of_current_month()
    current_22_stamp=time_cal.time_s_to_stamp(current_22)
    time_range_records=[]
    for item in records:
        for key in item:
            key_stamp=time_cal.str_to_stamp(key)
            if last_22_stamp < key_stamp < current_22_stamp:
                time_range_records.append({key:item[key]})
    # print(time_range_records)
    if len(time_range_records)==0:
        bills=0
    else:
        income_records=[]   #入账记录
        expend_records=[]   #消费记录
        for item in time_range_records:
            for ite in item:
                if '还款' in item[ite] or '收款' in item[ite]:
                    income_records.append(item[ite][2])
                else:
                    expend_records.append(item[ite][3])
                    expend_records.append(item[ite][2])
        if len(income_records)==0:income=0
        else:income=sum(income_records)
        if len(expend_records)==0:
            expend=0
        else:
            expend=sum(expend_records)
        if income>=expend:
            bills=0
        else:
            bills=expend-income
    bills_contect=[bills,time_range_records]    #相关信息生成列表
    return bills_contect


def check_file_month():
    """
    判断并生成本月账单文件的日期字符串
    :return:
    """
    mon=time_cal.get_22nd_of_last_month()
    file_month=str(mon).strip().split(' ')[0].strip().split('-')
    file_month.pop(2)
    res=''.join(file_month) #字符串萍姐
    return res




def main():
    """
    主函数
    :return:
    """
    dtd=time.strftime('%d')
    dtd=int(dtd)
    if dtd<=22: #判断时间是否过22日,如果未到22日,提醒用户
        print('本月生成账单日期未到,操作退出!')
        time.sleep(1)
    else:
        user_data=data_op.l_d()
        bill={}
        for item in user_data:
            bills_contect=generate_bills(item)
            bill[item]=bills_contect
        # print(bill)
        file_month=check_file_month()
        #如果过22日,遍历相关日期内的数据,并将数据写入文件,生产新的文件
        json.dump(bill,open('../db/{}_bills.json'.format(file_month),'w'),
                  ensure_ascii=False,indent=1)
        print('账单已生成,目录为:\033[31;1m../db/\033[0m,'
              '文件名称为:\033[31;1m{}_bills.json\033[0m'.format(file_month))
        log_admin.info('生成账单文件{}_bills.json'.format(file_month))
        time.sleep(1)

