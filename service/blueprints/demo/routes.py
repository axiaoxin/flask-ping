#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

import models
from utils import log
from utils import register_decorator_for_module_funcs
from . import handlers

demo_bp = Blueprint('demo', __name__)

decorators = [
    models.pw_auto_manage_connect(models.mysql_db),
    log.log_func_call
]
register_decorator_for_module_funcs(handlers, decorators)


demo_bp.route('/items', methods=['GET', 'POST'])(handlers.items)
demo_bp.route('/items/<int:id>', methods=['GET', 'DELETE', 'PUT'])(handlers.items)
