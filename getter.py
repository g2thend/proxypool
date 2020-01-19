#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/20/19 9:30 AM
# @Author  : yon
# @Email   :  @qq.com
# @File    : getter

from proxypool.db import sqlitedb
from proxypool.crawler import Crawler
from proxypool.setting import *
from proxypool.utils import cprint
import sys
import time


class Getter(object):
    def __init__(self):
        self.sqlite3 = sqlitedb()
        self.crawler = Crawler()
    def run(self):
        cprint('获取器开始执行')
        for callback_label in range(self.crawler.__CrawlFuncCount__):
            callback = self.crawler.__CrawlFunc__[callback_label]
            # 获取代理
            proxies = self.crawler.get_proxies(callback)
            sys.stdout.flush()
            cprint("插入数据到sqlite3 proxy 表")
            for proxy in proxies:
                self.sqlite3.add(list(proxy))


if __name__ == '__main__':
    get = Getter()
    get.run()
