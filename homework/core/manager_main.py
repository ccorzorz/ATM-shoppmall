#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
管理员操作主函数
"""
import sys,prettytable
sys.path.append('..')
from core import atm_admin_op,generate_bills

def show_menu():
    """
    定义显示菜单函数
    :return:
    """
    row=prettytable.PrettyTable()
    row.field_names=['新增账号','冻结用户','解冻用户','提升用户额度',
                     '查看所有用户','生成上月账单','退出程序']
    row.add_row([0,1,2,3,4,5,'q&quit'])
    print(row)


#函数名列表化
menu_list=[atm_admin_op.c_u,
           atm_admin_op.freeze_u,
           atm_admin_op.un_freeze_u,
           atm_admin_op.enhance_credit,
           atm_admin_op.show_all,
           generate_bills.main,
           atm_admin_op.logout_manage]


def main():
    """
    执行函数,登录成功后显示主菜单,用户选择对应的函数名后,执行对应的函数
    :return:
    """
    login_res=atm_admin_op.login()
    if login_res:
        while True:
            show_menu()
            inp=input('请选择操作对应的序列号:')
            if inp=='q' or inp=='quit':
                menu_list[6]()
            elif inp.isdigit():
                inp=int(inp)
                if inp<6:
                    menu_list[inp]()
                else:
                    print('选择有误,请重新输入.')
            else:
                print('选择有误,请重新输入.')

    else:
        print('登录失败!')


if __name__ == '__main__':
    main()