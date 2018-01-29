#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('tasks')
app.config_from_object('config')
logger = get_task_logger(__name__)


if __name__ == '__main__':
    app.start()
