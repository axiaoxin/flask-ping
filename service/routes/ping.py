from flask import Blueprint
from response import response
from utils.base import pw_auto_manage_connect, log_func_call
from models import mysql_db
from handlers.ping import demo


ping = Blueprint('ping', __name__)


@ping.route('/')
@log_func_call
@pw_auto_manage_connect(mysql_db)
def demo_route():
    data = demo()
    return response(data=data)
