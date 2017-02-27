from flask import Blueprint
from response import response
from utils.base import pw_auto_manage_connect
from models import mysql_db
from .handlers.demo import demo


ping_api = Blueprint('ping_api', __name__)


@ping_api.route('/')
def ping():
    return response(data='pong')


@ping_api.route('/demo')
@pw_auto_manage_connect(mysql_db)
def demo_route():
    data = demo()
    return response(data=data)
