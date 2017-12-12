# -*- coding:utf-8 -*-
import os

from decouple import config

DB_URL = config(
    'DB_URL',
    default=('mysql+pool+retry://root:root@localhost:3306/db_demo'
             '?max_connections=40&stale_timeout=300&charset=utf8mb4'))

DEBUG = config('DEBUG', default=False, cast=bool)
JSON_AS_ASCII = config('JSON_AS_ASCII', default=False, cast=bool)

SERVICE_NAME = config('SERVICE_NAME', default='flask-skeleton')
API_URL = config('API_URL', default='http://localhost:5000')
SENTRY_DSN = config('SENTRY_DSN', default=None)

LOG_PATH = config("LOG_PATH", default='/tmp/')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
LOG_FUNC_CALL = config('LOG_FUNC_CALL', default=True, cast=bool)
LOG_PEEWEE_SQL = config('LOG_PEEWEE_SQL', default=True, cast=bool)

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')
