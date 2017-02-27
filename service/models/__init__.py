#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import Model
from playhouse.shortcuts import RetryOperationalError
from playhouse.pool import PooledMySQLDatabase
from settings import DEBUG, DATABASE


class MySQLRetryDB(RetryOperationalError, PooledMySQLDatabase):
    pass


if DEBUG:
    mysql_db = MySQLRetryDB(**DATABASE['testing'])
else:
    mysql_db = MySQLRetryDB(**DATABASE['prod'])


class MySQLBaseModel(Model):
    '''使用mysql作为数据库的基础model'''
    class Meta:
        database = mysql_db
