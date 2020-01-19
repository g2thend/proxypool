#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/18/19 10:19 AM
# @Author  : yon
# @Email   : @qq.com
# @File    : db.py

from proxypool.error import PoolEmptyError
from proxypool.setting import proxyDbName, proxyDbPath
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE, PROTOCOL
from random import choice
from proxypool.utils import cprint
import re
import os
import sqlite3


class sqlitedb(object):
    """
    add　函数插入格式：
    insertproxy = ('114.114.114.114:8080', 'http')
    单个元组插入,对ipport和protocol 做约束处理,即各有一个不同也会插入,如果数据一样则不会插入成功
    """
    def __init__(self):
        """
        判断是否存在数据库,没有则创建
        并设置开关
        :rtype: object
        """
        self.dbPath = proxyDbPath + "/" + proxyDbName
        self.dbExists = os.path.exists(self.dbPath)
        self.dbCreated = self.checkdbexist()

    def checkdbexist(self):
        """
        没有数据库则创建
        创建数据库表proxy
        去重创建表:
        create  table proxy(id  INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ip  TEXT NOT NULL , port TEXT NOT NULL ,protocol  TEXT NOT NULL, score INTEGER NOT NULL  ,UNIQUE(ip,protocol));
        :rtype: object
        """
        if not self.dbExists:
            try:
                print("create proxydb: " + proxyDbName + " and table: proxy ")
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                c.execute('''CREATE TABLE proxy(id  INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ipport  TEXT NOT NULL ,protocol  TEXT NOT NULL, score INTEGER NOT NULL DEFAULT 100 ,UNIQUE(ipport, protocol))''')
                conn.commit()
                conn.close()
                cprint("pls get proxy ip to insert to the db ", color="red")
                return True
            except IOError:
                cprint("no proxydb !!", color="red")
        else:
            #后续添加检测是否存在proxy表
            return True

    def add(self, proxy):
        """
        判断数据库是否存在,代理写入数据库
        proxy = ('114.114.114.114:8080', 'http')
        :rtype: object
        """
        if not self.dbCreated:
            cprint("数据库不存在,请在setting检查数据库路径,并执行checkdbexist．．．．", color="red")
            return False
        else:
            try:
                if self.dbCreated:
                    conn = sqlite3.connect(self.dbPath)
                    c = conn.execute('INSERT INTO proxy(ipport, protocol)  VALUES (?,?)', proxy)
                    conn.commit()
                    conn.close()
                    cprint("success: add proxy ip  into db !!")
                    return True

            except Exception:
                print("add ip  into db WRONG!!")



    def random(self):
        """
        随机获取一个分数最高的代理,]
        如果没有则降序排列获取最高的一个
        :return :随机的一个代理
        """
        print(self.dbPath)
        if self.dbCreated:
            try:
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                getRandom = c.execute("select ipport,protocol from proxy where score=100")
                list = getRandom.fetchall()
                if list:
                    print(
                        "打印获取的随机代理,score=100"
                    )
                    # print(choice(list))
                    return choice(list)
                else:
                    getRandom = c.execute('''select  ipport,protocol from proxy where score>80''')
                    list = getRandom.fetchall()
                    if list:
                        return choice(list)
                    else:
                        cprint("no ip where score > 80 ", color="red")
                conn.close()
            except Exception as ex:
                print(type(ex))
                cprint("get random proxy  fail!!", color="red")
            finally:
                conn.close()
        else:
            cprint("no proxydb plse check...", color="red")

    def decrease(self, proxy):
        """
        减小指定ip的score
        :param proxy:
        """
        if self.dbCreated:
            try:
                conn = sqlite3.connect(self.dbPath)
                selectip = "select score  from  proxy where ipport='{0}'".format(proxy)
                c = conn.cursor()
                score = c.execute(selectip).fetchall()[0][0]
                if score and score > MIN_SCORE:
                    print(proxy, '当前分数', score, '减1')
                    xx = (score - 1, proxy)
                    c.execute('UPDATE proxy set score=?  WHERE ipport=?', xx)
                    print("update proxy:%s fromscore:%s  toscore:%s successfull!!" % (proxy, score, score-1))
            except Exception:
                print("WRONG: update  score of proxy ip!!")
            finally:
                conn.commit()
                conn.close()

    def exist(self, proxy):
        """
        检查指定ip是否存在
        :param proxy:
        :return: 是否存在
        """
        if self.dbCreated:
            try:
                conn = sqlite3.connect(self.dbPath)
                selectip = "select ipport,protocol from  proxy where ipport='{0}'".format(proxy)
                c = conn.cursor()
                proxylist = c.execute(selectip).fetchall()
                if proxylist:
                    print("proxy ip:%s check success"% proxylist)
                    return True
                else:
                    return False
            except Exception:
                print("WRONG: PROXY IP exist check!!")
            finally:
                conn.close()

    def max(self, proxy):
        """
        设置proxy为最大分数
        :param proxy:
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        if self.dbCreated:
            try:
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                c.execute('UPDATE proxy set score=?  WHERE ipport=?', (MAX_SCORE, proxy))
            except Exception:
                print("add ip  into db WRONG!!")
            finally:
                conn.commit()
                conn.close()

    def count(self):
        """
        :return: 代理的数量
        """
        if self.dbCreated:
            try:
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                selectcoutn = c.execute('''select * from proxy ''')
                return len(selectcoutn.fetchall())
            except Exception:
                print("add ip  into db WRONG!!")
            finally:
                conn.close()

    def all(self):
        """
        :return: 所有代理的列表
        """
        if self.dbExists:
            try:
                allist = []
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                selectcoutn = c.execute('''select ipport,protocol from proxy ''')
                for ipport in selectcoutn:
                    allist.append(ipport)
                return allist
            except Exception:
                print("WRONG: select all  proxy ip !!")
            finally:
                conn.close()

    def batch(self, start, stop):
        """

        :param start:
        :param stop:
        :return:
        """
        if self.dbExists:
            try:
                conn = sqlite3.connect(self.dbPath)
                c = conn.cursor()
                selectcoutn = c.execute('select ipport,protocol from proxy  where id>=? and id<=?', (start, stop))
                batchproxy = []
                for ipport in selectcoutn:
                    batchproxy.append(ipport)
                return batchproxy
            except Exception:
                print("WRONG: select all  proxy ip !!")
            finally:
                conn.close()


if __name__ == '__main__':
    proxy = ('180.122.41.108:9999', 'HTTPS')
    tt = sqlitedb()
    print(tt.random())
    # xx = tt.count()
    # print(xx)
    # tt.add(proxy)
    # xx = tt.count()
    # print(xx)

    # pp = "114.114.114.114:8080"
    # # check = tt.exist(pp)
    # # tt.max(pp)
    # # tt.decrease(pp)
    # # x = tt.count()
    # x = tt.all()
    # print(x)











