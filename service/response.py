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
    ResponseCode.SUCCESS: u'请求成功',
    ResponseCode.FAIL: u'请求失败',
    ResponseCode.BAD_REQUEST: u'请求参数错误',
    ResponseCode.API_NOT_FOUND: u'API不存在',
    ResponseCode.SERVER_ERROR: u'Internal Server Error',
}


def jsonify_(data):
    if DEBUG:
        js = json.dumps(data, ensure_ascii=False, indent=4)
    else:
        js = json.dumps(data, ensure_ascii=False, separators=[',', ':'])
    return Response(js, mimetype='application/json')


def response(code=ResponseCode.SUCCESS, msg=None, data=None):
    result = {'code': code}
    if msg:
        result['msg'] = msg
    else:
        result['msg'] = ResponseCodeMsg[code]

    if data is not None:
        result['data'] = data

    return jsonify_(result)
