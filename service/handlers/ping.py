#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.demo import Demo
from utils.base import get_serializable_model_dict, log_func_call


@log_func_call
def demo():
    data = [get_serializable_model_dict(i)
            for i in Demo.select()]
    return data
