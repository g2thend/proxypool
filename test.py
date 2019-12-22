#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/19/19 4:10 PM
# @Author  : yon
# @Email   : 201225144@qq.com
# @File    : test

import requests
from proxypool.db import sqlitedb
from proxypool.setting import *
import re

http = {"http": "http://42.159.10.142:8080"}
https = {"https": "http://223.199.29.80:9999"}
req = requests.get("http://httpbin.org/get", proxies=https, timeout=10)
print(req.text)
# http = {"http": "http://110.244.12.96:9999"}
# https = {"https": "http://49.70.89.55:9999"}
# response = requests.get("http://httpbin.org/get", proxies=https)
# print(response.text)
