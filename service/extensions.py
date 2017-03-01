#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from raven.contrib.flask import Sentry

from settings import SENTRY_DSN


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_pyfile('settings.py')

sentry = Sentry(app, dsn=SENTRY_DSN, logging=True,
                level=logging.DEBUG)
