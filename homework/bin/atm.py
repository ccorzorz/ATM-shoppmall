#!/usr/bin/env python
# -*-coding=utf-8-*-
# Auther:ccorz Mail:ccniubi@163.com Blog:http://www.cnblogs.com/ccorz/
# GitHub:https://github.com/ccorzorz
"""
ATM 终端入口
"""

import sys
sys.path.append('..')
from core import atm_run

if len(sys.argv)==2 and sys.argv[1]=='start':
    atm_run.main()
else:
    print('\"python atm.py start\" to starup programe!!')