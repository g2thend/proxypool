#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/18/19 10:19 AM
# @Author  : yon
# @Email   : @qq.com
# @File    : db.py

import json
import re
from pyquery import PyQuery as pq
from proxypool.utils import get_page
from proxypool.utils import cprint

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            cprint("成功获取到代理:" + str(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    tmp1 = ':'.join([ip, port])
                    tmp2 = (tmp1, "http")
                    yield tmp2

    def crawl_ip3366(self):
        for page in range(1, 4):
            print('Crawling', page)
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>\S*</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port, proto in re_ip_address:
                result = address + ':' + port
                tmp1 = result.replace(' ', '')
                tmp2 = (tmp1, proto)
                yield tmp2

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    temp1 = address_port.replace(' ', '')
                    temp2 = (temp1, "http")
                    yield temp2

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    find_protocol = re.compile('<td>(HTTPS*)</td>')
                    re_pro = find_protocol.findall(tr)
                    for address, port, protocol in zip(re_ip_address, re_port, re_pro):
                        address_port = address + ':' + port
                        tmp = (address_port, protocol)
                        yield tmp

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/free/wg'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                find_protocol = re.compile('<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>\s+<td>(.*?)</td>', re.S)
                re_pro = find_protocol.findall(trs[s])
                if re_pro[0][3].strip() == '':
                    re_pro = ["HTTP"]
                else:
                    re_pro = ["HTTPS"]
                for address, port, protocol in zip(re_ip_address, re_port, re_pro):
                    address_port = address + ':' + port
                    tmp = (address_port, protocol)
                    yield tmp

    # def crawl_xiladaili(self):
    # http://www.xiladaili.com/gaoni/  西拉免费代理
    # 网页获取的代理和通过程序获取的端口不一致,通过程序获取的端口是错误的
    # def crawl_data5u(self):
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'JSESSIONID=9C634C0DD99CB36A015698522C16C57F',
    #         'Host': 'www.data5u.com',
    #         'Referer': 'http://www.data5u.com/',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    #     req = requests.get("http://www.data5u.com/", headers=headers)
    #     soup = BeautifulSoup(req.text, 'lxml')
    #     uls = soup.select('ul .l2')
    #     for i in uls:
    #         li = i.get_text().split(sep='\n')
    #         proxy_ip = li[1]
    #         proxy_port = li[2]
    #         proxy_type = li[3]
    #         proxy_pro = li[4]
    #         address_port = proxy_ip + ':' + proxy_port
    #         tmp = (address_port, proxy_pro)
    #         yield tmp

    # def crawl_iphai(self):
    #     start_url = 'http://www.iphai.com/'
    #     html = get_page(start_url)
    #     if html:
    #         find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #         trs = find_tr.findall(html)
    #         for s in range(1, len(trs)):
    #             find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
    #             re_ip_address = find_ip.findall(trs[s])
    #             find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
    #             re_port = find_port.findall(trs[s])
    #             for address, port in zip(re_ip_address, re_port):
    #                 address_port = address + ':' + port
    #                 yield address_port.replace(' ', '')

    # def crawl_data5u(self):
    #     start_url = 'http://www.data5u.com/'
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
    #         'Host': 'www.data5u.com',
    #         'Referer': 'http://www.data5u.com/free/index.shtml',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    #     }
    #     html = get_page(start_url, options=headers)
    #     if html:
    #         ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>.*?<li>(\S+)</li>.*?<li>(https*)</li>', re.S)
    #         re_ip_address = ip_address.findall(html)
    #         for address, port, protocol in re_ip_address:
    #             result = address + ':' + port
    #             temp1 = result.replace(' ', '')
    #             tmp2 = (temp1, protocol)
    #             yield tmp2


# class Getter():
#     def __init__(self):
#         self.crawler = Crawler()
#
#     def run(self):
#         print('获取器开始执行')
#         for callback_label in range(self.crawler.__CrawlFuncCount__):
#             print(callback_label)
#             callback = self.crawler.__CrawlFunc__[callback_label]
#             print(callback)
#             # # 获取代理
#             # proxies = self.crawler.get_proxies(callback)
#             # sys.stdout.flush()
#             # for proxy in proxies:
#             #     self.redis.add(proxy)


if __name__ == '__main__':
    get = Crawler()
    proxies = get.crawl_data5u()
    # proxies <generator object Crawler.crawl_xicidaili at 0x7fa4f1edf410>
    # 为生成器,不能直接打印,需要展开来进行合并,然后组成元组,内容为列表,然后保存
    for proxy in proxies:
        print(proxy)
