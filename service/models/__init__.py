#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from contextlib import contextmanager
from functools import wraps

from peewee import Model
from playhouse.shortcuts import RetryOperationalError
from playhouse.pool import PooledMySQLDatabase
from playhouse.db_url import connect, schemes

from flask import abort

import utils
from settings import DB_URL


class MySQLRetryDB(RetryOperationalError, PooledMySQLDatabase):
    pass


schemes['mysql+pool+retry'] = MySQLRetryDB

mysql_db = connect(DB_URL)


class MySQLBaseModel(Model):

    class Meta:
        database = mysql_db


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


def pw_auto_manage_connect(db=mysql_db):
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
            data[k] = utils.datetime2str(v, '%Y-%m-%d')
        if isinstance(v, datetime.datetime):
            data[k] = utils.datetime2str(v)

    for field in pop:
        data.pop(field, None)

    return data


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)
