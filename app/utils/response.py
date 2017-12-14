#!/usr/bin/env python
# *- coding: utf-8 -*-
import json

from flask import Response
import settings
import stringcase
import log


class ResponseCode(object):
    SUCCESS = 0
    FAIL = -1
    PARAMS_ERROR = 400
    ENTRY_NOT_FOUND = 404
    SERVER_ERROR = 500


ResponseCodeMsg = {
    ResponseCode.SUCCESS: u'Succuss',
    ResponseCode.FAIL: u'Fail',
    ResponseCode.PARAMS_ERROR: u'Params Error',
    ResponseCode.ENTRY_NOT_FOUND: u'Entry Not Found',
    ResponseCode.SERVER_ERROR: u'Internal Server Error',
}


def keycase_convert(obj, func):
    if isinstance(obj, dict):
        return {func(k): keycase_convert(v, func) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [keycase_convert(elem, func) for elem in obj]
    else:
        return obj


def get_support_keycase():
    return [i for i in dir(stringcase)
            if i.endswith('case')]


def jsonify_(data):
    keycase = settings.JSON_KEYCASE
    if keycase:
        try:
            casefunc = getattr(stringcase, keycase)
            data = keycase_convert(data, casefunc)
        except AttributeError:
            log.warning(u'%s keycase is not supported, response default json. '
                        u'Supported keycase: %s'
                        % (keycase, get_support_keycase()))
    if settings.DEBUG:
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
