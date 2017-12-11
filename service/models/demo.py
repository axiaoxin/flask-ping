#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import peewee

from models import MySQLBaseModel
from models import get_object_or_404
from models import get_serializable_model_dict


class Demo(MySQLBaseModel):
    name = peewee.CharField()
    age = peewee.IntegerField()
    is_deleted = peewee.BooleanField(default=False)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'tb_demo'

    @classmethod
    def get_all_items(cls, serialized=True):
        data = cls.select().order_by(+cls.id)
        if serialized:
            data = [get_serializable_model_dict(i) for i in data]
        return data

    @classmethod
    def get_item_by_id(cls, id, serialized=True):
        data = get_object_or_404(cls, cls.id == id)
        if serialized:
            data = get_serializable_model_dict(data)
        return data

    @classmethod
    def add_item(cls, name, age, serialized=True):
        data = cls.create(name=name, age=age)
        if serialized:
            data = get_serializable_model_dict(data)
        return data
