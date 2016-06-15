#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
ATM 终端操作模块
"""
import sys
sys.path.append('..')
from core import data_op,format_num,pass_handler
from core.logger import *

#定义全局变量
tip={'user_name':None,'login_state':False}

def check_login(func):
    """
    定义一个装饰器,但后来发现逻辑中没什么乱用...搁置了,判断用户是否登录
    :param func:
    :return:
    """
    def inner(*args,**kwargs):
        if tip['login_state']:
            res=func(*args,**kwargs)
            return res
        else:
            print('\033[31;1m此操作需要登录!!!\033[0m')
    return inner

def freeze_count(args):
    """
    修改用户帐号状态的标志符函数
    :param args: 用户名
    :return: None
    """
    user_data=data_op.l_d()
    user_data[args][0]=0
    data_op.flush_d(user_data)

def login():
    user_data=data_op.l_d()
    inp=input('请输入账户名:')
    if user_data.get(inp)==None:
        print('{}账户错误,请重新输入..'.format(inp))
    else:
        if user_data[inp][0]==0:    #判断用户状态
            print('您的账户{}已被冻结,请联系管理员'.format(inp))
            log_access.warning('冻结用户{}尝试登录'.format(inp))
            return False
        else:
            i=0
            while i<4:
                if i==3:
                    freeze_count(inp)   #输入超过三次,冻结用户,修改状态标志符
                    print('您的账户{}已被冻结,请联系管理员'.format(inp))
                    log_access.warning('用户{}被冻结'.format(inp))
                    return False
                pwd_inp=input('请输入{}的密码:'.format(inp))
                pwd=pass_handler.md5_pwd(pwd_inp)   #密码加密匹配
                if pwd==user_data[inp][1]:
                    tip['user_name']=inp
                    tip['login_state']=True #修改全局变量字典
                    # print(tip)
                    print('登录成功!')
                    log_access.info('用户{}登录成功'.format(inp))
                    return True
                else:
                    print('密码输入有误,请重新输入.')
                    i+=1

if __name__ == '__main__':
    login()