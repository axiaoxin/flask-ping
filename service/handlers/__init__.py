#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import importlib
from utils.base import log_func_call
import inspect
import os


def _get_all_handler_modules():
    modules = []
    handlers_path = os.path.dirname(os.path.realpath(__file__))
    service_path = os.path.dirname(handlers_path)
    for root, dirs, files in os.walk(handlers_path):
        for f in files:
            if not f.endswith('.py') or f == '__init__.py':
                continue
            file_path = os.path.join(root, f)
            _, module_path = os.path.splitext(file_path)[0].split(service_path)
            module_name = module_path.replace(os.sep, '.')[1:]
            module = importlib.import_module(module_name)
            modules.append(module)
    return modules


def _register_decorator_for_all_handlers(decorator):
    '''将decorator注册到handlers下的所有函数'''
    modules = _get_all_handler_modules()
    for module in modules:
        for key, value in vars(module).iteritems():
            if (isinstance(value, types.FunctionType) and
                    inspect.getmodule(value).__name__.startswith('handlers')):
                vars(module)[key] = decorator(value)


_register_decorator_for_all_handlers(log_func_call)
