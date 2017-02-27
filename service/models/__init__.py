#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.shortcuts import RetryOperationalError
from playhouse.pool import PooledMySQLDatabase
from settings import DEBUG


class MySQLRetryDB(RetryOperationalError, PooledMySQLDatabase):
    pass


if DEBUG:
    mysql_db = MySQLRetryDB('test', user='root', password='root',
                            max_connections=40)
else:
    mysql_db = MySQLRetryDB('flask_ping', user='root', password='root',
                            max_connections=40)


class MySQLBaseModel(Model):
    '''使用mysql作为数据库的基础model'''
    class Meta:
        database = mysql_db
