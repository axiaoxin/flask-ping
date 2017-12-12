#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint

import models
import utils
from utils import log
from . import handlers

demo_bp = Blueprint('demo', __name__)

decorators = [
    models.pw_auto_manage_connect(models.mysql_db),
    utils.cache_get_response(),
    log.log_func_call
]
utils.register_decorator_for_module_funcs(handlers, decorators)


demo_bp.route('/items', methods=['GET', 'POST'])(handlers.items)
demo_bp.route('/items/<int:id>', methods=['GET', 'DELETE', 'PUT'])(handlers.items)
