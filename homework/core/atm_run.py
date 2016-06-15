#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
ATM 终端操作
"""
import sys,prettytable,time
sys.path.append('..')
from core.terminal_op import *
from core import terminal_op,terminal_repay,terminal_show_record,\
    terminal_transfers,terminal_view_credit,terminal_withdraw,\
    terminal_discover_bills,bills_rate



def logout():
    exit('系统退出')

#将函数名称对应写入列表方便用户选择
menu=[terminal_view_credit.view_credit,
      terminal_show_record.show_record,
      terminal_repay.repay,
      terminal_withdraw.withdraw,
      terminal_transfers.transfers,
      terminal_discover_bills.inquire_bills,
      bills_rate.inquire_rates,
      logout]


def main():
    """
    先执行登录函数,返回1时进入主菜单
    :return:
    """
    res=terminal_op.login()
    if res:
        row=prettytable.PrettyTable()
        row.field_names=['查看可用额度','查看消费记录','还款','提现','转账',
                         '查询本月账单','还款逾期情况查询','退出']
        row.add_row([0,1,2,3,4,5,6,'q&quit'])
        while True:
            print('\033[31;1m欢迎来到宇宙最屌老男孩支行\033[0m'.center(93,'*'))
            print(row)
            inp=input('请输入对应的操作序列号:')
            if inp.isdigit():
                inp=int(inp)
                if inp>7:
                    print('输入有误,请重新输入!!')
                else:
                    #如果用户选择正确,执行对应的函数
                    menu[inp](tip['user_name'])
                    time.sleep(1)
            elif inp.lower()=='q' or inp.lower()=='quit':
                logout()
            else:
                print('输入有误,请重新输入!!')
    else:
        pass


if __name__ == '__main__':
    main()