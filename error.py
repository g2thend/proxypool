#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 12/18/19 10:15 AM
# @Author  : yon
# @Email   : 201225144@qq.com
# @File    : error


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')

