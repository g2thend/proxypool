#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/20/19 2:30 PM
# @Author  : yon
# @Email   :  @qq.com
# @File    : tester

import requests
import json
from proxypool.db import sqlitedb
from proxypool.crawler import Crawler
from proxypool.setting import *
from proxypool.utils import cprint
import sys
import random
import time, re


class Tester(object):
    def __init__(self):
        self.sqlite = sqlitedb()
        self.public_ip = self.publicip()

    def publicip(self):
        req = requests.get("http://www.net.cn/static/customercare/yourip.asp")
        if req.status_code == 200:
            find_ip = re.compile('<h2>((\d{1,3})(\.\d{1,3}){3})</h2>')
            re_ip = find_ip.findall(req.text)
            return re_ip[0][0]
        else:
            cprint("获取公网IP失败", color="red")


    def veriy(self, proxy):
        cprint("正在验证" + str(proxy[0]))
        http = {"http": "http://" + proxy[0]}
        https = {"https": "http://" + proxy[0]}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Referer': 'https://www.google.com/'
        }
        time.sleep(0.3)
        try:
            if str(proxy[1]).lower() == "http":
                cprint("测试的代理ip" + str(http))
                response = requests.get(TEST_URL, proxies=http, timeout=10, headers=headers)
                if response.status_code == 200:
                    find_ip = re.compile('<h2>((\d{1,3})(\.\d{1,3}){3})</h2>')
                    re_ip1 = find_ip.findall(response.text)
                else:
                    cprint("代理测试公网IP失败获取公网IP失败", color="red")
                # if proxy[0] in str(response.text):
                # 222.129.38.93
                if self.public_ip != re_ip1[0][0]:
                    return True
                else:
                    return False
            else:
                cprint(https)
                response = requests.get(TEST_URL, proxies=https, timeout=10, headers=headers)
                if response.status_code == 200:
                    find_ip = re.compile('<h2>((\d{1,3})(\.\d{1,3}){3})</h2>')
                    re_ip2 = find_ip.findall(response.text)
                else:
                    cprint("代理测试公网IP失败", color="red")
                # if proxy[0] in str(response.text):
                if self.public_ip != re_ip2[0][0]:
                    return True
                else:
                    return False
        except Exception:
            cprint("代理有效性测试失败", color="red")
            return False

    def getheaders(self):
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
        cprint("代理有效性验证开始")
        print('\n')
        count = self.sqlite.count()
        cprint("共有代理数量:" + str(count))
        for i in range(0, count, BATCH_TEST_SIZE):
            start = i
            stop = min(i + BATCH_TEST_SIZE, count)
            print('正在测试第', start + 1, '-', stop, '个代理')
            time.sleep(1)
            testproxy = self.sqlite.batch(start, stop)
            print(testproxy)
            for proxy in testproxy:
                testresult = self.veriy(proxy)
                if testresult:
                    cprint(str(proxy[0]) + "可用")
                    self.sqlite.max(proxy[0])
                else:
                    self.sqlite.decrease(proxy[0])
                    cprint(str(proxy[0]) + "分数降级", color="red")


if __name__ == '__main__':
    test = Tester()
    test.run()
