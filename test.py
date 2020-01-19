#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/19/19 4:10 PM
# @Author  : yon
# @Email   :  @qq.com
# @File    : test

import requests
from proxypool.db import sqlitedb
from proxypool.setting import *

http = {"http": "http://95.67.47.94:53281"}
https = {"https": "http://62.148.67.110:81"}
req = requests.get("http://www.net.cn/static/customercare/yourip.asp", proxies=http, timeout=10)
# req = requests.get("http://httpbin.org/get", proxies=http)
if req.status_code == 200:
    print(req.text)
else:
    print("获取失败")





