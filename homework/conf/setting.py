#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
配置文件,配置交易费率字典,消费记录函数,以及日志的文件和等级等信息
"""
import sys,time,logging,datetime
sys.path.append('..')
from core import data_op,logger

dt=time.strftime('%Y-%m-%d %H:%M:%S')

trans_rate={'提现':0.05,'转账':0.05,'还款':0,'支付':0,'收款':0}

def record(user_name,TransType,business,amounts):
    user_data=data_op.l_d()
    rates=trans_rate[TransType]*amounts
    user_data[user_name][4].append({dt:[TransType,business,amounts,rates]})
    data_op.flush_d(user_data)
    return True

LOG_LEVEL=logging.DEBUG
LOG_TYPE={'access':'access.log','trans':'trans.log','admin':'admin.log'}
