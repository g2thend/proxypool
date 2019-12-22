#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/20/19 2:30 PM
# @Author  : yon
# @Email   : 201225144@qq.com
# @File    : tester

import requests
import json
from proxypool.db import sqlitedb
from proxypool.crawler import Crawler
from proxypool.setting import *
import sys
import random
import time


class Tester(object):
    def __init__(self):
        self.sqlite = sqlitedb()

    def veriy(self, proxy):
        print("正在验证" + proxy[0])
        http = {"http": "http://" + proxy[0]}
        https = {"https": "http://" + proxy[0]}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        time.sleep(0.3)
        try:
            if str(proxy[1]).lower() == "http":
                print(http)
                response = requests.get(TEST_URL, proxies=http, timeout=10, headers=headers)
                # if proxy[0] in str(response.text):
                # 222.129.38.93
                if "222.129.38.93" not in str(response.text):
                    return True
                else:
                    return False
            else:
                print(https)
                response = requests.get(TEST_URL, proxies=https, timeout=10, headers=headers)
                # if proxy[0] in str(response.text):
                if "222.129.38.93" not in str(response.text):
                    return True
                else:
                    return False
        except Exception:
            print("代理有效性测试失败")
            return False

    def getheaders():
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            ]
        UserAgent = random.choice(user_agent_list)
        return UserAgent

    def run(self):
        print("代理有效性验证开始")
        count = self.sqlite.count()
        print("数量:", count)
        for i in range(0, count, BATCH_TEST_SIZE):
            start = i
            stop = min(i + BATCH_TEST_SIZE, count)
            print('正在测试第', start + 1, '-', stop, '个代理')
            testproxy = self.sqlite.batch(start, stop)
            print(testproxy)
            for proxy in testproxy:
                print("正在测试代理:", proxy)
                testresult = self.veriy(proxy)
                if testresult:
                    print("代理可用", proxy[0])
                    self.sqlite.max(proxy[0])
                else:
                    self.sqlite.decrease(proxy[0])
                    print("代理分数降级")


if __name__ == '__main__':
    test = Tester()
    test.run()
