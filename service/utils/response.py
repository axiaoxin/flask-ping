#!/usr/bin/env python
# *- coding: utf-8 -*-
import json

from flask import Response
from settings import DEBUG


class ResponseCode(object):
    SUCCESS = 0
    FAIL = -1
    BAD_REQUEST = 400
    API_NOT_FOUND = 404
    SERVER_ERROR = 500


ResponseCodeMsg = {
    ResponseCode.SUCCESS: u'Succuss',
    ResponseCode.FAIL: u'Fail',
    ResponseCode.BAD_REQUEST: u'Bad Request',
    ResponseCode.API_NOT_FOUND: u'Entry Not Found',
    ResponseCode.SERVER_ERROR: u'Internal Server Error',
}


def jsonify_(data):
    if DEBUG:
        js = json.dumps(data, ensure_ascii=False, indent=4)
    else:
        js = json.dumps(data, ensure_ascii=False, separators=[',', ':'])
    return Response(js, mimetype='application/json')


def response(data=None, code=ResponseCode.SUCCESS, msg=None):
    result = {'code': code, 'data': data}
    if msg:
        result['msg'] = msg
    else:
        result['msg'] = ResponseCodeMsg.get(code, '')

    return jsonify_(result)


def keyerror_response(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            data = u'Need params:{0}'.format(e)
            log.warning(data)
            return response(code=ResponseCode.BAD_REQUEST, data=data)

    return wrap
