#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
日志模块
"""
import sys,logging
sys.path.append('..')
from conf.setting import *



def logger(log_type):
    """
    定义日志模块
    :param log_type: 日志的用户
    :return:
    """
    logger=logging.getLogger(log_type)
    logger.setLevel(LOG_LEVEL)

    ch=logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    fh=logging.FileHandler('../log/{}'.format(LOG_TYPE[log_type]))
    fh.setLevel(LOG_LEVEL)

    formatter=logging.Formatter('%(asctime)s - %(name)s -'
                                ' %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

#将日志实例化,防止进入循环后多次刷新日志
log_trans=logger('trans')
log_access=logger('access')
log_admin=logger('admin')