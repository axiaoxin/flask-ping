import os
import sys
from multiprocessing import cpu_count

import settings

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
app_path = os.path.join(root_path, 'app')
sys.path.append(app_path)

proc_name = settings.SERVICE_NAME
bind = settings.API_BIND
workers = cpu_count() * 2 + 1
worker_class = 'gevent'
reload = settings.DEBUG
pidfile = '/tmp/flask-skeleton.pid'
raw_env = []
pythonpath = ','.join([app_path, root_path])
accesslog = os.path.join(settings.LOG_PATH,
                         settings.SERVICE_NAME + '-gunicorn-access.log')
access_log_format = '%(t)s %(h)s "%(f)s" "%(a)s" "%(r)s" %(s)s %(p)s %(L)s'
errorlog = os.path.join(settings.LOG_PATH,
                        settings.SERVICE_NAME + '-error.log')
loglevel = settings.LOG_LEVEL
