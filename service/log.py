#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from settings import DEFAULT_LOG_FILE


def get_logger(logger_name=__name__, logger_type=None, log_file=None):
    '''save log to diffrent file by seting logger type:
    WARING,ERROR, if no set, save log to default log file'''
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')

    if log_file is None:
        log_file = DEFAULT_LOG_FILE

    if logger_type == 'ERROR':
        path, ext = os.path.splitext(log_file)
        log_file = path + '.err' + ext
    elif logger_type == 'WARNING':
        path, ext = os.path.splitext(log_file)
        log_file = path + '.war' + ext

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


app_logger = get_logger(logger_name='app_log')
warning_logger = get_logger(logger_type='WARNING', logger_name='app_warning')
error_logger = get_logger(logger_type='ERROR', logger_name='app_error')


def debug(msg, *args, **kwargs):
    app_logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    app_logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    warning_logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    error_logger.exception(msg, *args, **kwargs)
