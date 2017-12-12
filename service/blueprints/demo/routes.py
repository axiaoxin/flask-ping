#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

import models
import utils
from utils import log
from utils import memoize
from . import handlers

demo_bp = Blueprint('demo', __name__)

decorators = [
    models.pw_auto_manage_connect(models.mysql_db),
    memoize.cache_get_response(max_age=3),
    log.log_func_call
]
utils.register_decorator_for_module_funcs(handlers, decorators)


demo_bp.route('/items', methods=['GET', 'POST'])(handlers.items)
demo_bp.route('/items/<int:id>', methods=['GET', 'DELETE', 'PUT'])(handlers.items)
