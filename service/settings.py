# -*- coding:utf-8 -*-
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

API_URL = config('API_URL', default='http://localhost')

DEFAULT_LOG_FILE = config(
    "DEFAULT_LOG_FILE", default='/var/log/flask-ping/app.log')
CRONTAB_LOG_FILE = config(
    "CRONTAB_LOG_FILE", default='/var/log/flask-ping/crontab.log')

JSON_AS_ASCII = False

SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_POOL_RECYCLE = 60 * 20
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 1
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = config(
    'DEFAULT_DB',
    default='mysql+pymysql://user:passwd@host:port/db_name')  # noqa
SQLALCHEMY_BINDS = {
    'OTHER_DB': config(
        'OTHER_DB',
        default='mysql+pymysql://user:passwd@host:port/other_db_name'),  # noqa
}

MAIL_SENDER = 'flask-demo@axiaoxin.com'
