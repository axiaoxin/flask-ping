from flask import Blueprint
from response import response


ping_api = Blueprint('ping_api', __name__)


@ping_api.route('/')
def ping():
    return response(data='pong')
