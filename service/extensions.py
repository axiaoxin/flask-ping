# -*- coding:utf-8 -*-
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
mail = Mail(app)

app.config.from_pyfile('settings.py')
