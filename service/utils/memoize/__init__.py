"""Redis lock and store wrapper.

The lock implementation was mostly lifted from
http://chris-lamb.co.uk/2010/06/07/distributing-locking-python-and-redis/

"""
import time
import shelve
import urlparse
from functools import wraps

from flask import request
from redis import Redis

from .core import Memoizer
import settings


class Lock(object):
    def __init__(self, db, key, expires=60):
        """
        Distributed locking using Redis SETNX and GETSET.

        Usage::

            with Lock('my_lock'):
                print "Critical section"

        :param  expires     We consider any existing lock older than
                            ``expires`` seconds to be invalid in order to
                            detect crashed clients. This value must be higher
                            than it takes the critical section to execute.
        :param  timeout     If another client has already obtained the lock,
                            sleep for a maximum of ``timeout`` seconds before
                            giving up. A value of 0 means we never wait.
        """

        self.db = db
        self.key = key
        self.expires = expires

    def acquire(self, timeout):
        delay = 0.1
        while timeout >= 0:
            expires = time.time() + self.expires + 1

            if self.db.setnx(self.key, expires):
                # We gained the lock; enter critical section
                return True

            current_value = self.db.get(self.key)

            # We found an expired lock and nobody raced us to replacing it
            if current_value and float(current_value) < time.time() and \
               self.db.getset(self.key, expires) == current_value:
                return True

            timeout -= delay
            time.sleep(min(timeout, delay))
            delay *= 2

        return False

    def release(self):
        self.db.delete(self.key)


def wrap(redis, lock_class=Lock):
    def lock(key):
        return lock_class(redis, key + '.lock')

    db = shelve.Shelf(redis)
    db.lock = lock
    return db


redis_client = Redis.from_url(settings.REDIS_URL)

redis_memoize = Memoizer(wrap(redis_client))


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
