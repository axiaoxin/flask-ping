#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import datetime
from functools import wraps
from contextlib import contextmanager

from response import response, ResponseCode
from log import get_logger

logger = get_logger(__name__)


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


def keyerror_response(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            data = u'缺少参数:{0}'.format(e)
            logger.warning(data)
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
        logger.exception(str(e))
        raise
    finally:
        session.close()


def pw_auto_manage_connect(db):
    def deco(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                db.connect()
                data = func(*args, **kwargs)
                return data
            finally:
                if not db.is_closed():
                    db.close()
        return wrap
    return deco
