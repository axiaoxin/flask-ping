#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def timestamp2str(ts, str_format='%Y-%m-%d %H:%M:%S', utc=False):
    if utc:
        dt = datetime.datetime.utcfromtimestamp(ts)
    else:
        dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime(str_format)


def datetime2str(dt, str_format='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(str_format)


def format_timestr(timestr, from_format, to_format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(timestr, from_format).strftime(to_format)


def get_serializable_model_dict(model, pop=[]):
    if not model:
        return
    for k, v in model.__dict__.iteritems():
        if isinstance(v, datetime.date):
            model.__dict__[k] = datetime2str(v, '%Y-%m-%d')
        if isinstance(v, datetime.datetime):
            model.__dict__[k] = datetime2str(v)

    for field in pop:
        model.__dict__.pop(field, None)
    model.__dict__.pop('_sa_instance_state', None)

    return model.__dict__


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
def db_session_scope(session, commit=False):
    """Provide a transactional scope around a series of operations."""
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
