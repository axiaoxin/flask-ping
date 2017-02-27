# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from response import response, ResponseCode
from ping_api import ping_api


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_pyfile('settings.py')


@app.errorhandler(404)
def api_not_found(error):
    return response(ResponseCode.API_NOT_FOUND)


@app.errorhandler(500)
def server_error(error):
    return response(ResponseCode.SERVER_ERROR)


@app.route('/')
def hello_world():
    path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), '.packtime')
    if not os.path.exists(path):
        return 'hello!'
    with open(path) as packtime:
        return packtime.read()


app.register_blueprint(ping_api, url_prefix='/ping')


if __name__ == '__main__':
    app.run('0.0.0.0')
