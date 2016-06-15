#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz

import hashlib

def md5_pwd(pwd):
    """
    为了防止解密,hashlib.md5时加入自己的字段
    将密码转化为 md5形式
    :param pwd: 密码明文
    :return: 加密后的密码
    """
    hash=hashlib.md5(bytes('odlboy',encoding='utf8'))
    hash.update(bytes(pwd,encoding='utf8'))
    res=hash.hexdigest()
    return res


