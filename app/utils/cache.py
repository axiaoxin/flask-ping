# coding:utf-8
import cPickle
import time
import urlparse
from functools import wraps

from flask import request

import settings
from services import redis
from utils import get_func_name
from utils.log import app_logger


def _generate_key(namespace, tag, **kwargs):
    prefix = 'cached_call'
    if namespace == 'funcs':
        key = ':'.join(
            field
            for field in
            [prefix, namespace, tag, kwargs['funcname'], kwargs['params']]
            if field)
    elif namespace == 'views':
        key = ':'.join(
            field
            for field in
            [prefix, namespace, tag, kwargs['url_path'], kwargs['url_query']]
            if field)
    return key


def cached_call(cached_over_ms=settings.CACHED_OVER_EXEC_MILLISECONDS,
                expire=settings.CACHED_EXPIRE_SECONDS,
                tag='',
                namespace='views'):
    prefix = 'cached_call'

    def cached_deco(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if not settings.CACHED_CALL:
                return func(*func_args, **func_kwargs)

            if namespace == 'views':
                if request.method == 'GET':
                    url = urlparse.urlsplit(request.url)
                    key = _generate_key(
                        namespace, tag, url_path=url.path, url_query=url.query)
                else:
                    return func(*func_args, **func_kwargs)
            elif namespace == 'funcs':
                params = '%s&%s' % (str(func_args), str(func_kwargs))
                funcname = get_func_name(func)
                key = _generate_key(
                    namespace, tag, funcname=funcname, params=params)
            try:
                data = redis.get(key)
            except Exception as e:
                app_logger.exception(e)
                return func(*func_args, **func_kwargs)
            else:
                if data is not None:
                    app_logger.debug(u'data from cache:%r' % key)
                    return cPickle.loads(data)
                else:
                    start_time = time.time()
                    result = func(*func_args, **func_kwargs)
                    exec_time = (time.time() - start_time) * 1000
                    if exec_time > cached_over_ms:
                        try:
                            redis.setex(key, cPickle.dumps(result), expire)
                            app_logger.debug(u'cached:%r' % key)
                        except Exception as e:
                            app_logger.exception(e)
                    return result

        return wrapper

    return cached_deco


def get_redislock(name,
                  timeout=settings.REDIS_LOCK_TIMEOUT,
                  blocking_timeout=None):
    ''' Useage:

    lock = get_redislock('print_arg:%s' % arg, blocking_timeout=1)
    if lock.acquire():
        try:
            do_something
        finally:
            lock.release()
    else:
        logger.warning('blocking')

    '''
    key = 'lock:' + name
    lock = redis.lock(
        name=key, timeout=timeout, blocking_timeout=blocking_timeout)
    return lock
