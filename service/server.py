# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from extensions import app
from response import response, ResponseCode

from ping_api import ping_api


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
    with open(path) as packtime:
        return packtime.read()


app.register_blueprint(ping_api, url_prefix='/ping')


if __name__ == '__main__':
    app.run('0.0.0.0')
