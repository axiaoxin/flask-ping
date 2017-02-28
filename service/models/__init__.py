#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.shortcuts import RetryOperationalError
from playhouse.pool import PooledMySQLDatabase
from playhouse.db_url import connect, schemes
from settings import DB_URL


class MySQLRetryDB(RetryOperationalError, PooledMySQLDatabase):
    pass


schemes['mysql+pool+retry'] = MySQLRetryDB


mysql_db = connect(DB_URL)


class MySQLBaseModel(Model):
    '''使用mysql作为数据库的基础model'''
    class Meta:
        database = mysql_db
