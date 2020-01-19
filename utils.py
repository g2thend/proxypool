#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/19/19 4:01 PM
# @Author  : yon
# @Email   :  @qq.com
# @File    : utils

import requests
from requests.exceptions import ConnectionError

base_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    headers = dict(base_headers, **options)
    print('正在抓取', url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None


def cprint(text, color="green"):
    if text is None:
        print("\033[1;31m%s \033[0m" % "no text to print")
        return
    if color == "green":
        print("\033[1;32m%s \033[0m" % text)
    elif color == "red":
        print("\033[1;31m%s \033[0m" % text)
    elif color == "yellow":
        print("\033[1;33m%s \033[0m" % text)
    elif color == "blue":
        print("\033[1;34m%s \033[0m" % text)


if __name__ == '__main__':
    cprint("skskskks")
