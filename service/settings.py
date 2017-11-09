# -*- coding:utf-8 -*-
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

API_URL = config('API_URL', default='http://localhost:5000')

DEFAULT_LOG_FILE = config(
    "DEFAULT_LOG_FILE", default='/tmp/app.log')
CRONTAB_LOG_FILE = config(
    "CRONTAB_LOG_FILE", default='/tmp/crontab.log')

JSON_AS_ASCII = False

DATABASE = {
    'testing': {
        'database': 'test',
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'charset': 'utf8mb4',
        'max_connections': 40
    },
    'prod': {
        'database': 'prod',
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'charset': 'utf8mb4',
        'max_connections': 40
    }
}
