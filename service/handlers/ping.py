#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.ping import Demo
from utils.base import get_serializable_model_dict


def demo():
    data = [get_serializable_model_dict(i)
            for i in Demo.select()]
    return data
