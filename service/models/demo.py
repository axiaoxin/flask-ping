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
    def get_item(cls, id=None, order_by='id', order_type='desc', serialized=True):
        if id is not None:
            data = get_object_or_404(cls, cls.id == id)
        else:
            order_field = getattr(cls, order_by)
            if order_type.lower() == 'asc':
                data = cls.select().order_by(-order_field)
            else:
                data = cls.select().order_by(+order_field)
        if serialized:
            if isinstance(data, peewee.SelectQuery):
                data = [get_serializable_model_dict(i) for i in data]
            else:
                data = get_serializable_model_dict(data)
        return data

    @classmethod
    def add_item(cls, name, age, serialized=True):
        data = cls.create(name=name, age=age)
        if serialized:
            data = get_serializable_model_dict(data)
        return data

    @classmethod
    def delete_item(cls, id, real=False):
        if real:
            query = cls.delete().where(cls.id == id)
        else:
            query = cls.update(is_deleted=True).where(cls.id == id)
        count = query.execute()
        data = {'deleted_count': count}
        return data

    @classmethod
    def update_item(cls, id, name=None, age=None, is_deleted=None, serialized=True):
        data = get_object_or_404(cls, cls.id == id)
        if name:
            data.name = name
        if age:
            data.age = age
        if is_deleted:
            data.is_deleted = is_deleted
        data.save()
        if serialized:
            data = get_serializable_model_dict(data)
        return data
