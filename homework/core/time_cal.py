#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
时间处理模块
"""
import datetime,time
def get_22nd_of_last_month():
    """
    获取上个月第一天的日期，然后加21天就是22号的日期
    :return: 返回日期
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    if month==1:
        month=12
        year-=1
    else:
        month-=1
    res=datetime.datetime(year,month,1)+datetime.timedelta(days=21)
    return res


def get_22nd_of_next_month():
    """
    获取下个月的22号的日期
    :return: 返回日期
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    if month==12:
        month=1
        year+=1
    else:
        month+=1
    res=datetime.datetime(year,month,1)+datetime.timedelta(days=21)
    return res


def get_10th_of_current_month():
    """
    获取本月的10号的日期
    :return: 返回日期
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    res=datetime.datetime(year,month,11)
    return res


def get_22nd_of_current_month():
    """
    获取本月22号的日期
    :return: 返回日期
    """
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    res=datetime.datetime(year,month,22)
    return res

def time_s_to_stamp(args):
    """
    将datetime日期格式，先timetuple()转化为struct_time格式
    然后time.mktime转化为时间戳
    :param args:    datetime时间格式数据
    :return:    时间戳格式数据
    """
    res=time.mktime(args.timetuple())
    return res

def str_to_stamp(args):
    """
    将时间字符串格式转化为时间戳格式
    :param args: 时间字符串格式
    :return: 时间戳数据
    """
    r=time.strptime(args,'%Y-%m-%d %H:%M:%S')
    res=time.mktime(r)
    return res
