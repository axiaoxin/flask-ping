#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import types
import inspect

import settings
import log


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


def register_decorators_on_module_funcs(modules, decorators):
    '''将decorator自动注册到module中的所有函数
    函数中设置__nodeco__属性为False或者以下划线开头的名称
    则不自动注册任何装饰器
    eg:
        def func():
            pass
        func.__nodeco__ = True
    '''
    if not isinstance(modules, (list, tuple)):
        modules = [modules]
    if not isinstance(decorators, (list, tuple)):
        decorators = [decorators]
    for m in modules:
        for funcname, func in vars(m).iteritems():
            if (isinstance(func, types.FunctionType)
                    and not funcname.startswith('_')
                    and func.__module__ == m.__name__):
                if getattr(func, '__nodeco__', False):
                    continue
                for deco in decorators:
                    if settings.DEBUG:
                        log.debug('register %s on %s.%s'
                                  % (deco.__name__, m.__name__, funcname))
                    func = deco(func)
                    vars(m)[funcname] = func