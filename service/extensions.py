# -*- coding:utf-8 -*-
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)

app.config.from_pyfile('settings.py')
