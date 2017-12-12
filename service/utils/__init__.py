#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import types
import inspect
import urlparse
from functools import wraps

from flask import request

import settings
from memoize import redis_memoize


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
    函数中设置__nodeco__属性为False或者以下划线开头的名称
    则不自动注册任何装饰器
    eg:
        def func():
            pass
        func.__nodeco__ = True
    '''
    if not isinstance(module, (list, tuple)):
        module = [module]
    if not isinstance(decorator, (list, tuple)):
        decorator = [decorator]
    for m in module:
        for funcname, func in vars(m).iteritems():
            if (isinstance(func, types.FunctionType) and
                    not funcname.startswith('_')):
                if getattr(func, '__nodeco__', False):
                    continue
                for deco in decorator:
                    func = deco(func)
                    vars(m)[funcname] = func


def cache_get_response(namespace='views', max_age=60):
    def _cache(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if settings.CACHE_GET_RESPONSE and request.method == 'GET':
                url = urlparse.urlsplit(request.url)
                key = ':'.join(field for field in [url.path, url.query]
                               if field)
                return redis_memoize.get(
                    str(key),
                    func,
                    func_args,
                    func_kwargs,
                    max_age=max_age,
                    namespace=namespace)
            return func(*func_args, **func_kwargs)

        return wrapper

    return _cache
