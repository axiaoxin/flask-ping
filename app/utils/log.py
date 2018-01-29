#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
from gevent.monkey import patch_all
patch_all()  # noqa

import time
import os
import logging
import sys
from logging import raiseExceptions
from logging import Logger
from functools import wraps

from extensions import sentry
import settings
import utils


class AppLogger(Logger):
    def __init__(self, name, level=logging.NOTSET):
        super(AppLogger, self).__init__(name, level)

    def callHandlers(self, record):
        """
        Pass a record to all relevant handlers.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. If no handler was found, output a one-off error
        message to sys.stderr. Stop searching up the hierarchy whenever a
        logger with the "propagate" attribute set to zero is found - that
        will be the last logger whose handlers are called.
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if hdlr.name == 'console':
                    if record.levelno >= hdlr.level:
                        hdlr.handle(record)
                else:
                    if record.levelno == hdlr.level:
                        hdlr.handle(record)
            if not c.propagate:
                c = None  # break out
            else:
                c = c.parent
        if (
                found == 0
        ) and raiseExceptions and not self.manager.emittedNoHandlerWarning:  # noqa
            sys.stderr.write("No handlers could be found for logger"
                             " \"%s\"\n" % self.name)
            self.manager.emittedNoHandlerWarning = 1


def init_logger(logger_name,
                logfile_name=__name__,
                logging_level=logging.DEBUG,
                log_path=settings.LOG_PATH):
    '''save log to diffrent file by deffirent log level into the log path
    and print all log in console'''
    logging.setLoggerClass(AppLogger)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')

    log_files = {
        logging.DEBUG: os.path.join(log_path, logfile_name + '-debug.log'),
        logging.INFO: os.path.join(log_path, logfile_name + '-info.log'),
        logging.WARNING: os.path.join(log_path, logfile_name + '-warning.log'),
        logging.ERROR: os.path.join(log_path, logfile_name + '-error.log'),
        logging.CRITICAL:
        os.path.join(log_path, logfile_name + '-critical.log')  # noqa
    }

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    for log_level, log_file in log_files.items():
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.name = "console"
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = init_logger('werkzeug', settings.SERVICE_NAME)
if settings.LOG_PEEWEE_SQL:
    pw_logger = init_logger('peewee', settings.SERVICE_NAME)


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)
    if isinstance(msg, Exception):
        sentry.captureException()


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)
    if isinstance(msg, Exception):
        sentry.captureException()


def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)
    if isinstance(msg, Exception):
        sentry.captureException()


def exception(msg, *args, **kwargs):
    logger.exception(msg, *args, **kwargs)
    if isinstance(msg, Exception):
        sentry.captureException()


def _log_func_call(func, use_time, *func_args, **func_kwargs):
    arg_names = func.func_code.co_varnames[:func.func_code.co_argcount]
    args = func_args[:len(arg_names)]
    defaults = func.func_defaults or ()
    args = args + defaults[len(defaults) - (func.func_code.co_argcount - len(
        args)):]
    params = zip(arg_names, args)
    args = func_args[len(arg_names):]
    if args:
        params.append(('args', args))
    if func_kwargs:
        params.append(('kwargs', func_kwargs))
    func_name = utils.get_func_name(func)
    func_call = u'{func_name}({params}) {use_time}ms'.format(
        func_name=func_name,
        params=', '.join('%s=%r' % p for p in params),
        use_time=use_time * 1000)
    info(func_call)


def log_func_call(func):
    '''Decorator to log function call'''

    @wraps(func)
    def wrapper(*func_args, **func_kwargs):
        if settings.LOG_FUNC_CALL:
            start_time = time.time()
            data = func(*func_args, **func_kwargs)
            use_time = time.time() - start_time
            gevent.spawn(_log_func_call, func, use_time, *func_args,
                         **func_kwargs)
            return data
        return func(*func_args, **func_kwargs)

    return wrapper
