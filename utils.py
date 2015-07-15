#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'
from functools import wraps

#计数闭包
def close_func(start=0):
    c = [start]
    def _count():
        c[0] += 1
        return c[0]
    return _count

count = close_func()

#计数修饰器
def count_method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print '---------------'
        print 'total: %s' % count()
        func(*args, **kwargs)
    return wrapper