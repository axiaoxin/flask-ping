#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import types
import inspect


def is_ipv4(ip):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return True
    return False


def datetime2timestamp(dt, is_int=True):
    ts = time.mktime(dt.timetuple())
    if is_int:
        ts = int(ts)
    return ts


def timestamp2str(ts, str_format='%Y-%m-%d %H:%M:%S'):
    dt = datetime.datetime.utcfromtimestamp(ts)
    return dt.strftime(str_format)


def datetime2str(dt, str_format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(str_format)


def register_decorator_for_module_funcs(module, decorator):
    '''将decorator自动注册到module中的所有函数
    函数中设置__nodeco__属性为False则不自动注册任何装饰器
    eg:
        def func():
            pass
        func.__nodeco__ = True'''
    if not isinstance(module, (list, tuple)):
        module = [module]
    if not isinstance(decorator, (list, tuple)):
        decorator = [decorator]
    for m in module:
        for funcname, func in vars(m).iteritems():
            if (isinstance(func, types.FunctionType) and
                    not inspect.getmodule(func).__name__.startswith('_')):
                if getattr(func, '__nodeco__', False):
                    continue
                for deco in decorator:
                    vars(m)[funcname] = deco(func)
