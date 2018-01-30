# coding:utf-8
import cPickle
import time
import urlparse
from contextlib import contextmanager
from functools import wraps

from flask import request
from redis import Redis
from redis.exceptions import LockError

import settings
import utils

redis_client = Redis.from_url(settings.REDIS_URL)


def cached(expire=settings.CACHED_EXPIRE_SECONDS, tag='', namespace='views'):
    def cached_deco(func):
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):
            if not settings.CACHED_CALL:
                return func(*func_args, **func_kwargs)

            if namespace == 'views':
                if request.method == 'GET':
                    url = urlparse.urlsplit(request.url)
                    key = ':'.join(
                        field
                        for field in [namespace, tag, url.path, url.query]
                        if field)
                else:
                    return func(*func_args, **func_kwargs)
            elif namespace == 'funcs':
                params = '%s&%s' % (str(func_args), str(func_kwargs))
                funcname = utils.get_func_name(func)
                key = ':'.join(field
                               for field in [namespace, tag, funcname, params]
                               if field)

            data = redis_client.get(key)
            if data is None:
                start_time = time.time() * 1000
                result = func(*func_args, **func_kwargs)
                if time.time(
                ) * 1000 - start_time > settings.CACHED_OVER_EXEC_MILLISECONDS:
                    redis_client.setex(key, cPickle.dumps(result), expire)
                return result
            return cPickle.loads(data)

        return wrapper

    return cached_deco


@contextmanager
def distlock(name, timeout=settings.REDIS_LOCK_TIMEOUT, blocking_timeout=None):
    key = 'distlock:' + name
    lock = redis_client.lock(
        name=key,
        timeout=timeout,
        blocking_timeout=blocking_timeout)
    if lock.acquire():
        yield
        lock.release()
