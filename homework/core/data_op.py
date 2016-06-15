#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
数据库操作函数配置
"""
import json
def l_d():
    """
    读 atm 用户数据库
    :return:
    """
    user_data=json.load(open('../db/atm_cart_db.json','r'))
    return user_data

def flush_d(args):
    """
    写入 ATM用户数据
    :param args:  新的用户数据
    :return:  True
    """
    json.dump(args,open('../db/atm_cart_db.json','w'),ensure_ascii=False,indent=1)
    return True

def l_a_d():
    """
    加载管理员数据库
    :return:
    """
    admin_data=json.load(open('../db/atm_admin_db.json','r'))
    return admin_data