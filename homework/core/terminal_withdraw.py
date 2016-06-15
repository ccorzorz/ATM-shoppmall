#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
提现模块
"""
import sys
sys.path.append('..')
from core import data_op,format_num
from conf.setting import *
from core.logger import *

def withdraw(args):
    """
    提现函数,与转账模块基本一样,但无需验证目标用户
    :param args: 用户名
    :return:
    """
    user_data=data_op.l_d()
    able_amount=user_data[args][3]
    max_amount_2=user_data[args][2]/2
    if able_amount>=max_amount_2:
        able_wd_amount=max_amount_2
    else:
        able_wd_amount=able_amount
    print('您的可用提现额度为:{}'.format(format_num.fn(able_wd_amount)))
    for i in range(4):
        if i ==3:
            print('输入格式错误超过3次,退出提现操作.')
            break
        amount=input('请输入提现金额:')
        if amount.isdigit():
            amount=int(amount)
            if amount>able_wd_amount:
                print('最高取现额度为{},已超支,'
                      '退出操作!'.format(format_num.fn(able_wd_amount)))
                log_trans.info('{}提现操作失败'.format(args))
                break
            else:
                user_data[args][3]-=amount+amount*trans_rate['提现']
                data_op.flush_d(user_data)
                print('现可消费额度为:'
                      '{}'.format(format_num.fn(user_data[args][3])))
                record(args,'提现','终端机',amount)
                log_trans.info('{}成功提现{}'.format(args,amount))
                break
        else:
            i+=1
            print('输入格式错误,还有{}次机会'.format(3-i))
