#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import peewee

from models import MySQLBaseModel
from models import get_object_or_404
from models import model2dict


class Demo(MySQLBaseModel):
    name = peewee.CharField()
    age = peewee.IntegerField()
    is_deleted = peewee.BooleanField(default=False)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'tb_demo'

    @classmethod
    def get_item(cls, id=None, order_by='id', order_type='desc', to_dict=True):
        if id is not None:
            data = get_object_or_404(cls, cls.id == id)
        else:
            order_field = getattr(cls, order_by)
            if order_type.lower() == 'asc':
                data = cls.select().order_by(-order_field)
            else:
                data = cls.select().order_by(+order_field)
        if to_dict:
            if isinstance(data, peewee.SelectQuery):
                data = [model2dict(i) for i in data]
            else:
                data = model2dict(data)
        return data

    @classmethod
    def add_item(cls, name, age, to_dict=True):
        data = cls.create(name=name, age=age)
        if to_dict:
            data = model2dict(data)
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
    def update_item(cls, id, name=None, age=None, is_deleted=None, to_dict=True):
        data = get_object_or_404(cls, cls.id == id)
        if name:
            data.name = name
        if age:
            data.age = age
        if is_deleted:
            data.is_deleted = is_deleted
        data.save()
        if to_dict:
            data = model2dict(data)
        return data
