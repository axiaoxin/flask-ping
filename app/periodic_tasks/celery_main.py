#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from celery.utils.log import get_task_logger

celery_app = Celery('tasks')
celery_app.config_from_object('celery_config')
logger = get_task_logger(__name__)


if __name__ == '__main__':
    celery_app.start()
