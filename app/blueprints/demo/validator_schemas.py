#!/usr/bin/env python
# -*- coding: utf-8 -*-

items_post = {
    'name': {
        'type': 'string',
        'empty': False,
        'maxlength': 64,
        'forbidden': ['root', 'admin'],
        'required': True,
    },
    'age': {
        'type': 'integer',
        'min': 1,
        'max': 100,
        'required': True,
    },
}

items_put = {
    'name': {
        'type': 'string',
        'empty': False,
        'maxlength': 64,
        'forbidden': ['root', 'admin'],
        'required': False,
    },
    'age': {
        'type': 'integer',
        'min': 1,
        'max': 100,
        'required': False,
    },
}
