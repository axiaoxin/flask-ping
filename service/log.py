#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers
import sys
from logging import raiseExceptions
from logging import Logger

from extensions import sentry
from settings import LOG_PATH


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
        if (found == 0) and raiseExceptions and not self.manager.emittedNoHandlerWarning:  # noqa
            sys.stderr.write("No handlers could be found for logger"
                             " \"%s\"\n" % self.name)
            self.manager.emittedNoHandlerWarning = 1


def _init_logger(logfile_name=__name__, log_path=LOG_PATH):
    '''save log to diffrent file by deffirent log level into the log path
    and print all log in console'''
    logging.setLoggerClass(AppLogger)
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        '%Y-%m-%d %H:%M:%S')

    log_files = {
        logging.DEBUG: os.path.join(log_path, logfile_name + '-debug.log'),
        logging.INFO: os.path.join(log_path, logfile_name + '-info.log'),
        logging.WARNING: os.path.join(log_path, logfile_name + '-warning.log'),
        logging.ERROR: os.path.join(log_path, logfile_name + '-error.log'),
        logging.CRITICAL: os.path.join(log_path, logfile_name + '-critical.log')  # noqa
    }
    logger = logging.getLogger('werkzeug')
    logger.setLevel(logging.DEBUG)
    for log_level, log_file in log_files.items():
        file_handler = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight')  # noqa
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.name = "console"
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = _init_logger()


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
