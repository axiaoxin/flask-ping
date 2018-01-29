#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from raven.contrib.flask import Sentry
from werkzeug.contrib.fixers import ProxyFix

import settings

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(settings)

sentry = Sentry(app, dsn=settings.SENTRY_DSN)
