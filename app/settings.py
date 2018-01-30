# -*- coding:utf-8 -*-
import os

from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
JSON_AS_ASCII = config('JSON_AS_ASCII', default=False, cast=bool)
JSON_KEYCASE = config('JSON_KEYCASE', default=None)

SERVICE_NAME = config('SERVICE_NAME', default='flask-skeleton')
API_BIND = config('API_URL', default='localhost:5000')
DB_URL = config(
    'DB_URL',
    default=('mysql+pool+retry://root:root@localhost:3306/test'
             '?max_connections=40&stale_timeout=300&charset=utf8mb4'))
SENTRY_DSN = config('SENTRY_DSN', default=None)

LOG_LEVEL = config('LOG_LEVEL', default='info')
LOG_PATH = config("LOG_PATH", default='/tmp/')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
LOG_FUNC_CALL = config('LOG_FUNC_CALL', default=True, cast=bool)
LOG_PEEWEE_SQL = config('LOG_PEEWEE_SQL', default=False, cast=bool)

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CACHED_CALL = config('CACHED_CALL', default=True, cast=bool)
CACHED_OVER_EXEC_MILLISECONDS = config(
    'CACHED_OVER_EXEC_MILLISECONDS', default=800, cast=int)
CACHED_EXPIRE_SECONDS = config('CACHED_EXPIRE_SECONDS', default=60, cast=int)
REDIS_LOCK_VALIDITY_MILLISECONDS = config(
    'REDIS_LOCK_VALIDITY_MILLISECONDS', default=1000, cast=int)
EXCEPTION_RETRY_COUNT = config('EXCEPTION_RETRY_COUNT', default=2, cast=int)
