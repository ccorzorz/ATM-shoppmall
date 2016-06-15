#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

def fn(args):
    """
    将金额转化为人民币模式,带逗号分隔,保留小数点两位,四舍五入
    :param args:
    :return:
    """
    num='{:,.2f}'.format(args)
    return num

