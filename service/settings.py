# -*- coding:utf-8 -*-
import os

from decouple import config


DEBUG = config('DEBUG', default=False, cast=bool)

API_URL = config('API_URL', default='http://localhost:5000')

SENTRY_DSN = config('SENTRY_DSN', default=None)

LOG_PATH = config("LOG_PATH", default='/tmp/')
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

JSON_AS_ASCII = False

DB_URL = config('DB_URL')
