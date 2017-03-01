# -*- coding:utf-8 -*-
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

API_URL = config('API_URL', default='http://localhost:5000')

SENTRY_DSN = config('SENTRY_DSN', default=None)

DEFAULT_LOG_FILE = config(
    "DEFAULT_LOG_FILE", default='/tmp/app.log')

JSON_AS_ASCII = False

DB_URL = config('DB_URL')
