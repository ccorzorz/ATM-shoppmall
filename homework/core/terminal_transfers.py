#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
转账模块
"""
import sys
sys.path.append('..')
from core import data_op,format_num,veri_code
from conf.setting import *
from core.logger import *

def transfers(args):
    #载入用户数据
    user_data=data_op.l_d()
    able_amount=user_data[args][3]
    max_amount_2=user_data[args][2]/2
    #可用额度如果大于信用额度的二分之一,则可转账额度为可用额度
    if able_amount>=max_amount_2:
        able_wd_amount=max_amount_2
    else:#否则,可转账额度为可用额度
        able_wd_amount=able_amount
    print('您的可用转账额度为:{}'.format(format_num.fn(able_wd_amount)))
    t_user_name=input('请输入您要转入的账户名称:')
    #判断用户转账目标是否存在于本系统数据库中
    if user_data.get(t_user_name)==None:
        print('本银行无此账户信息,请核实信息后再进行转账...')
    else:
        #转账操作
        for i in range(4):
            if i ==3:
                print('输入格式错误超过3次,退出提现操作.')
                break
            amount=input('请输入转账金额:')
            if amount.isdigit():
                amount=int(amount)
                #判断金额是否超支
                if amount>able_wd_amount:
                    print('最高转账额度为{},已超支,'
                          '退出操作!'.format(format_num.fn(able_wd_amount)))
                    break
                else:
                    #如不超支,转账,先验证码验证
                    res=veri_code.check_veri()
                    if res:
                        #修改数据库信息
                        user_data[args][3]-=amount+amount*trans_rate['转账']
                        user_data[t_user_name][3]+=amount
                        data_op.flush_d(user_data)
                        print('转账成功,现可消费额度为:'
                              '{}'.format(format_num.fn(user_data[args][3])))
                        record(args,'转账','终端机',amount)
                        record(t_user_name,'收款',args,amount)
                        log_trans.info('{}向{}成功转账{}'.format(args,t_user_name,amount))
                        break
                    else:
                        print('验证失败!转账操作失败!!')
                        log_trans.info('{}向{}转账失败'.format(args,t_user_name))
                        break
            else:
                i+=1
                print('输入格式错误,还有{}次机会'.format(3-i))
