#!/usr/bin/env python
# -*- coding: utf-8 -*-
import peewee
from models import MySQLBaseModel


class Demo(MySQLBaseModel):
    name = peewee.CharField()
    age = peewee.IntegerField()
    is_deleted = peewee.BooleanField()
    created_at = peewee.DateTimeField()
    updated_at = peewee.DateTimeField()

    class Meta:
        db_table = 'tb_demo'
