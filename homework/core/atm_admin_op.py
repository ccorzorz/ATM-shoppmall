#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
管理员操作模块,
show_all 查看所有账户信息
c_u 新建用户
freeze_u   冻结账户
un_freeze   解冻账户
enhance_credit 提升额度
logout 退出登录
"""
import sys
sys.path.append('..')
from core import data_op,format_num,pass_handler
from core.logger import *


def show_all():
    """
    显示所有用户信息
    :return:  None
    """
    user_data=data_op.l_d()
    print('现有账户额度以及状态'.center(30,'*'))
    for item in user_data:
        if user_data[item][0]==0:
            user_data[item][0]='冻结'
        else:
            user_data[item][0]='正常'
        print('{:10s}{:15s}{:10s}'.format(item,
                                          format_num.fn(user_data[item][2]),
                                          user_data[item][0]))

def c_u():
    """
    创建用户,额度,以及密码,密码使用 md5处理,并记录 log 日志,修改相关数据库
    :return: None
    """
    user_data=data_op.l_d()
    while True:
        inp=input('请输入用户帐号,输入 b 返回主菜单:')
        if inp=='b':
            break
        elif user_data.get(inp)==None:
            while True:
                balance=input('请输入初始额度,必须为整数的数字:')
                if balance.isdigit():
                    balance=int(balance)
                    break
                else:
                    print('输入有误,重新输入...')
            pwd_inp=input('请输入用户的密码:')
            pwd=pass_handler.md5_pwd(pwd_inp)
            user_data[inp]=[1,pwd,balance,balance,[]]
            data_op.flush_d(user_data)
            print('帐号{}信息添加成功,额度为{}'.format(inp,format_num.fn(balance)))
            log_admin.info('添加{}帐号信息,额度:{}'.format(inp,balance))
            break
        else: #如果用户存在,提示用户
            print('帐号{}已存在,请重新输入.'.format(inp))





def freeze_u():
    """
    冻结用户,修改相关数据库
    :return:  None
    """
    user_data=data_op.l_d()
    while True:
        show_all()
        inp=input('请输入要冻结的账户,输入 b 返回主菜单:')
        if inp=='b':
            break
        elif user_data.get(inp)==None:  #如无账户,提示管理员
            print('无{}账户信息'.format(inp))
        else:
            if user_data[inp][0]==0:
                print('账户{}已被冻结,无需重复操作'.format(inp))
                break
            else:
                user_data[inp][0]=0
                data_op.flush_d(user_data)
                print('账户{}冻结成功!'.format(inp))
                log_admin.info('冻结账户{}'.format(inp))
                break


def un_freeze_u():
    """
    解冻账户,与冻结账户操作相反,并修改数据库
    :return:
    """
    user_data=data_op.l_d()
    freeze_user_list=[]
    for item in user_data:
        if user_data[item][0]==0:
            freeze_user_list.append(item)
    if len(freeze_user_list)==0:
        print('无被冻结账户,无需继续操作.')
        return False
    else:
        print('已被冻结用户如下'.center(20,'*'))
        for item in freeze_user_list:
            print(item)
    while True:
        inp=input('请输入要解除冻结状态的账户,输入 b 返回主菜单:')
        if inp=='b':
            break
        elif inp not in freeze_user_list:
            print('冻结状态账户中无{}账户信息'.format(inp))
        else:
            if user_data[inp][0]==1:
                print('账户{}未冻结,无需重复操作'.format(inp))
                break
            else:
                user_data[inp][0]=1
                data_op.flush_d(user_data)
                print('账户{}解冻成功!'.format(inp))
                # loggerin
                log_admin.info('解冻账户{}'.format(inp))
                break


def enhance_credit():
    """
    提升用户额度,并修改用户信用额度以及可用额度信息
    :return: None
    """
    user_data=data_op.l_d()
    ex_flag=1
    while ex_flag:
        show_all()
        inp=input('请输入用户名,输入 b 返回主菜单:')
        if inp=='b':
            break
        if user_data.get(inp) == None:  #判断用户是否存在
            print('无{}账户信息,请重新输入.'.format(inp))
        else:
            # print(user_data[inp])
            amount=user_data[inp][2]
            f_amount=format_num.fn(amount)
            print('账户{}目前最高额度为{}'.format(inp,f_amount))
            while ex_flag:
                want_amount=input('请输入要提升的额度，需要数字并且是整数：')
                if want_amount.isdigit():
                    want_amount=int(want_amount)
                    if want_amount<=amount:
                        print('提升目标额度小于或等于目前额度，无需提升')
                    else:
                        dif_amount=want_amount-user_data[inp][2]
                        user_data[inp][2]=want_amount
                        user_data[inp][3]+=dif_amount
                        data_op.flush_d(user_data)
                        print('额度提升成功，目前{}额度为{}'.format(inp,format_num.fn(want_amount)))
                        log_admin.info('账户{}提升额度为{}'.format(inp,want_amount))
                        ex_flag=0
                else:
                    print('输入有误，请重新输入.')


def logout_manage():
    """
    退出信息,并记录日志
    :return:
    """
    log_admin.info('admin退出登录')
    exit('程序退出！')

def login():
    """
    登录信息
    :return:
    """
    admin_data=data_op.l_a_d()
    inp=input('请输入管理员帐号:')
    if admin_data.get(inp)==None:
        print('管理员角色中无用户{}'.format(inp))
    else:
        i=0
        while i<4:
            if i ==3:
                print('输入超过三次,关闭登录.')
                return False
            pwd=input('请输入{}的密码:'.format(inp))
            if pwd==admin_data[inp]:
                return True
            else:
                i+=1


