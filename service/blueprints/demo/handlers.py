#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from models.demo import Demo
from utils.response import response
from utils.cache import cached


def items(id=None):
    if request.method == 'GET' and id is None:
        order_by = request.values.get('order_by', 'id')
        order_type = request.values.get('order_type', 'desc')
        data = Demo.get_item(order_by=order_by, order_type=order_type)
    elif request.method == 'GET' and id is not None:
        data = Demo.get_item(id)
    elif request.method == 'POST':
        item = request.get_json()
        data = Demo.add_item(**item)
    elif request.method == 'DELETE' and id is not None:
        data = Demo.delete_item(id)
    elif request.method == 'PUT':
        item = request.get_json()
        data = Demo.update_item(id, **item)
    return response(data)
