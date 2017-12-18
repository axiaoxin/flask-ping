# coding:utf-8
import time
import urlparse
import cPickle
from contextlib import contextmanager
from functools import wraps

from flask import request, Response
from redis import Redis

import settings


redis_client = Redis.from_url(settings.REDIS_URL)


def cached(expire=settings.CACHED_EXPIRE_SECONDS, key_prefix='', namespace='views'):
    def cached_deco(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if not settings.CACHED_CALL:
                return func(*func_args, **func_kwargs)

            if namespace == 'views':
                if request.method == 'GET':
                    url = urlparse.urlsplit(request.url)
                    key = ':'.join(field for field in [namespace, key_prefix, url.path, url.query]
                                   if field)
                else:
                    return func(*func_args, **func_kwargs)
            elif namespace == 'funcs':
                key = ':'.join(field for field in [namespace, key_prefix, func.__name__,
                               str(func_args), str(func_kwargs)] if field)

            data = redis_client.get(key)
            if data is None:
                start_time = time.time() * 1000
                result = func(*func_args, **func_kwargs)
                if time.time() * 1000 - start_time > settings.CACHED_OVER_EXEC_MILLISECONDS:
                    redis_client.setex(key, cPickle.dumps(result), expire)
                return result
            return cPickle.loads(data)

        return wrapper

    return cached_deco


@contextmanager
def distlock(name, timeout=None, blocking=False, blocking_timeout=None):
    try:
        lock = redis_client.lock(name='distlock:' + name, timeout=timeout)
        lock.acquire(blocking=blocking, blocking_timeout=blocking_timeout)
        yield lock
    finally:
        lock.release()