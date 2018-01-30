# !/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import g

from utils.response import response, ResponseCode
from blueprints.demo import demo_bp
from extensions import app, sentry
import settings


@app.errorhandler(404)
def api_not_found(error):
    return response(code=ResponseCode.ENTRY_NOT_FOUND)


@app.errorhandler(Exception)
def server_error(error):
    if settings.SENTRY_DSN:
        data = {
            'sentry_event_id': g.sentry_event_id,
            'public_dsn': sentry.client.get_public_dsn('http')
        }
    else:
        data = None
    return response(data, ResponseCode.SERVER_ERROR)


@app.route('/')
def hello_world():
    return response(data='Hello!')


app.register_blueprint(demo_bp, url_prefix='/demo')

if __name__ == '__main__':
    app.run()
