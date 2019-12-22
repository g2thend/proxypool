#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/20/19 2:19 PM
# @Author  : yon
# @Email   : 201225144@qq.com
# @File    : imorter

# 手动录入代理
# 未测试
from proxypool.db import sqlitedb
importer = sqlitedb()


def importproxy(proxy):
    result = importer.add(proxy)
    print(proxy)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入代理, 输入exit退出读入')
    while True:
        proxy = input("代理ip,格式为 ip:port")
        protocol = input("代理协议:http或https")
        temp = (proxy, protocol)
        if proxy == 'exit':
            break
        set(list(temp))


if __name__ == '__main__':
    scan()

