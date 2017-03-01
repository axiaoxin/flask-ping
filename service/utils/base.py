#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
from gevent.monkey import patch_all
patch_all()  # noqa

import inspect
import re
import time
import datetime
from functools import wraps
from contextlib import contextmanager

from response import response, ResponseCode
import log


def is_ipv4(ip):
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return True
    return False


def get_sep_list(s, sep=','):
    return s.split(sep)


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


def get_serializable_model_dict(model, pop=[], orm='peewee'):
    if not model:
        return

    data = model.__dict__
    if orm == 'sqlalchemy':
        data.pop('_sa_instance_state', None)
    elif orm == 'peewee':
        data = model._data

    for k, v in data.iteritems():
        if isinstance(v, datetime.date):
            data[k] = datetime2str(v, '%Y-%m-%d')
        if isinstance(v, datetime.datetime):
            data[k] = datetime2str(v)

    for field in pop:
        data.pop(field, None)

    return data


def get_func_name(func, full=True):
    if full:
        return '{}.{}'.format(inspect.getmodule(func).__name__,
                              func.__name__)
    else:
        return func.__name__


def keyerror_response(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            data = u'缺少参数:{0}'.format(e)
            log.warning(data)
            return response(code=ResponseCode.BAD_REQUEST, data=data)
    return wrap


@contextmanager
def sa_session_scope(session, commit=False):
    """Provide a transactional scope around a series of operations
    for sqlalchemy."""
    try:
        yield session
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        log.error(e)
        raise
    finally:
        session.close()


def pw_auto_manage_connect(db):
    def deco(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                # db.get_conn().ping(True)
                db.connect()
                data = func(*args, **kwargs)
                return data
            finally:
                if not db.is_closed():
                    db.close()
        return wrap
    return deco


def _log_func_call(func, use_time, *func_args, **func_kwargs):
    arg_names = func.func_code.co_varnames[:func.func_code.co_argcount]
    args = func_args[:len(arg_names)]
    defaults = func.func_defaults or ()
    args = args + defaults[len(defaults) -
                           (func.func_code.co_argcount - len(args)):]
    params = zip(arg_names, args)
    args = func_args[len(arg_names):]
    if args:
        params.append(('args', args))
    if func_kwargs:
        params.append(('kwargs', func_kwargs))
    func_name = get_func_name(func)
    func_call = u'{func_name}({params}) {use_time}ms'.format(
            func_name=func_name,
            params=', '.join('%s=%r' % p for p in params),
            use_time=use_time * 1000)
    log.info(func_call)


def log_func_call(func):
    '''Decorator to log function call'''
    @wraps(func)
    def wrapper(*func_args, **func_kwargs):
        start_time = time.time()
        data = func(*func_args, **func_kwargs)
        use_time = time.time() - start_time
        gevent.spawn(_log_func_call, func, use_time, *func_args, **func_kwargs)
        return data
    return wrapper
