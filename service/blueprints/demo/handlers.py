#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from models.demo import Demo
from utils.response import response
from utils.response import ResponseCode
from utils.cache import cached
from blueprints import validator
from . import validator_schemas


def items(id=None):
    if request.method == 'GET' and id is None:
        order_by = request.values.get('order_by', 'id')
        order_type = request.values.get('order_type', 'desc')
        data = Demo.get_item(order_by=order_by, order_type=order_type)
    elif request.method == 'GET' and id is not None:
        data = Demo.get_item(id)
    elif request.method == 'POST':
        item = request.get_json()
        if not validator.validate(item, validator_schemas.items_post):
            return response(validator.errors, ResponseCode.PARAMS_ERROR)
        data = Demo.add_item(**item)
    elif request.method == 'DELETE' and id is not None:
        data = Demo.delete_item(id)
    elif request.method == 'PUT':
        item = request.get_json()
        if not validator.validate(item, validator_schemas.items_put):
            return response(validator.errors, ResponseCode.PARAMS_ERROR)
        data = Demo.update_item(id, **item)
    return response(data)
