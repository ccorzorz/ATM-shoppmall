#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
支付接口
"""
import sys,time
sys.path.append('..')
from core import terminal_op,data_op,format_num,veri_code
from conf.setting import *
from core.logger import *

def pay_api(args,business):
    """
    支付接口主函数
    :param args: 支付金额
    :param business: 支付商家
    :return: True:支付成功  False:支付失败
    """
    print('\033[31;1m欢迎使用宇宙最屌银行支付接口,支付需要登录\033[0m')
    res=terminal_op.login() #支付前先登录
    if res:
        user_data=data_op.l_d()
        tip=terminal_op.tip
        user_name=tip['user_name']
        balance=user_data[tip['user_name']][3]
        #提示用户可用额度
        print('您的可用额度为{}'.format(format_num.fn(balance)))
        if balance < args:  #额度不足,提醒
            print('\033[31;1m可用额度不足,请使用其他方式支付\033[0m')
            log_trans.info('{}调用支付接口,额度不足,支付失败'.format(user_name))
            time.sleep(1)
            return False
        else:
            #如果额度够,验证码验证,并修改相关用户数据信息
            user_data[tip['user_name']][3]-=args
            res=veri_code.check_veri()
            if res:
                data_op.flush_d(user_data)
                record(user_name,'支付',business,args)
                print('支付完成')
                log_trans.info('{}支付调用,用'
                                     '户{}支付{}'.format(business,user_name,args))
                return True
            else:
                print('验证码失败,支付失败,loser!!')
                time.sleep(1)
                return False
    else:
        #登录失败
        print('支付失败,请用其他方式支付,或者联系银行行长!')
        log_trans.info('支付接口支付失败,登录验证不通过')
        time.sleep(1)
        return False

if __name__ == '__main__':
    pay_api(100,'test')