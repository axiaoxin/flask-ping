#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
sys.path.append('..')
from celery import Celery
from celery.utils.log import get_task_logger
from raven import Client
from raven.contrib.celery import register_signal, register_logger_signal
import settings

celery_app = Celery('tasks')
celery_app.config_from_object('celery_config')
logger = get_task_logger(__name__)

sentry = Client(settings.SENTRY_DSN)
register_logger_signal(sentry)
register_logger_signal(sentry, loglevel=logging.INFO)
register_signal(sentry)
register_signal(sentry, ignore_expected=True)


if __name__ == '__main__':
    celery_app.start()
