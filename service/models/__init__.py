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
    '''ʹ��mysql��Ϊ���ݿ�Ļ���model'''
    class Meta:
        database = mysql_db
