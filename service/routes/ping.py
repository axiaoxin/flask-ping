from flask import Blueprint
from response import response
from utils.base import pw_auto_manage_connect
from models import mysql_db
from handlers.ping import demo


ping = Blueprint('ping', __name__)


@ping.route('/')
def ping_route():
    return response(data='pong')


@ping.route('/demo')
@pw_auto_manage_connect(mysql_db)
def demo_route():
    data = demo()
    return response(data=data)
