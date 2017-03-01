# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask import g

from response import response, ResponseCode
from routes.ping import ping
from extensions import app, sentry


@app.errorhandler(404)
def api_not_found(error):
    return response(ResponseCode.API_NOT_FOUND)


@app.errorhandler(500)
def server_error(error):
    data = {
        'sentry_event_id': g.sentry_event_id,
        'public_dsn': sentry.client.get_public_dsn('http')
    }
    return response(ResponseCode.SERVER_ERROR, data=data)


@app.route('/')
def hello_world():
    path = os.path.join(os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))), '.packtime')
    if not os.path.exists(path):
        return 'hello!'
    with open(path) as packtime:
        return packtime.read()


app.register_blueprint(ping, url_prefix='/ping')


if __name__ == '__main__':
    app.run()
