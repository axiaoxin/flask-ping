from multiprocessing import cpu_count
import os

app_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'app'
)

proc_name = 'flask-skeleton'
bind = '127.0.0.1:5000'
workers = cpu_count() * 2 + 1
worker_class = 'gevent'
reload = False
pidfile = '/tmp/flask-skeleton.pid'
raw_env = []
pythonpath = app_path
accesslog = '/tmp/gunicorn-access.log'
access_log_format = '%(t)s %(h)s "%(r)s" %(s)s %(p)s %(L)s'
errorlog = '/tmp/flask-skeleton-error.log'
