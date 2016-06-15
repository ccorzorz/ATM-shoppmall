#!/usr/bin/env python3
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
ATM管理后台入口
"""

import sys
sys.path.append('..')
from core import manager_main
if len(sys.argv)==2 and sys.argv[1]=='start':
    manager_main.main()
else:
    print('\"python3 credit_manage.py start\" to starup programe')
# manager_main.main()