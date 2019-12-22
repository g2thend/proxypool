#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/18/19 10:04 AM
# @Author  : yon
# @Email   : 201225144@qq.com
# @File    : setting

# Sqlite3数据库名称
proxyDbName = "proxypool.db"
proxyDbPath = "/home/baixiaoxu/PycharmProjects/pytthon-tt/proxypool"


# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
PROTOCOL = "http"

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://httpbin.org/get'

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 20