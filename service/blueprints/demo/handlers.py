#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from models.demo import Demo
from utils import response

def items(id=None):
    if request.method == 'GET' and id is None:
        data = Demo.get_all_items()
    elif request.method == 'GET' and id is not None:
        data = Demo.get_item_by_id(id)
    else:
        item = request.get_json()
        data = Demo.add_item(**item)
    return response.response(data=data)
