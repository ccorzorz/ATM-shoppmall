#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
还款模块
"""
import sys
sys.path.append('..')
from core import data_op,format_num
from conf.setting import *
from core.logger import *

def repay(args):
    """
    还款函数
    :param args:
    :return:
    """
    user_data=data_op.l_d()
    #如果可用额度大于等于信用额度,提示用户无需还款
    if user_data[args][3] >= user_data[args][2]:
        print('无欠款,无需还款!!!')
    else:
        #计算需还款额度
        need_repay=user_data[args][2]-user_data[args][3]
        print('您所需还款金额为:\033[31;1m{}\033[0m'.format(format_num.fn(need_repay)))
        while True:
            amount=input('请输入还款金额:')
            if amount.isdigit():
                amount=int(amount)
                if amount>need_repay:   #判断如果大于需还款金额,用户选择
                    inp=input('还款金额多余所需还款金额,是否继续?'
                          '\033[32;1m回车或y 继续,back 或者 b 为返回\033[0m:')
                    if len(inp)==0 or inp.lower() == 'y':
                        #修改用户账户信息
                        user_data[args][3]+=amount
                        data_op.flush_d(user_data)
                        print('还多了...还款完成!,目前可用信用金额'
                              '为\033[31;1m{}\033[0m'.format
                              (format_num.fn(user_data[args][3])))
                        record(args,'还款','终端机',amount)
                        log_trans.info('{}成功还款{}'.format(args,amount))
                        break
                    elif inp.lower() == 'b' or inp.lower()=='back':
                        break
                else:
                    #修改用户账户信息
                    user_data[args][3]+=amount
                    data_op.flush_d(user_data)
                    print('还款完成!目前可用信用金额'
                              '为\033[31;1m{}\033[0m'.format
                          (format_num.fn(user_data[args][3])))
                    record(args,'还款','终端机',amount)
                    log_trans.info('{}成功还款{}'.format(args,amount))
                    break
            else:
                print('输入有误,请重新输入.')

