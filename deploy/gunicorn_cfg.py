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
reload = True
pidfile = '/tmp/flask-skeleton.pid'
raw_env = []
pythonpath = app_path
accesslog = '/tmp/gunicorn-access.log'
access_log_format = '%(t)s %(h)s %(s)s "%(r)s" %(b)s "%(f)s" "%(a)s" "%({Header}i)s"'
errorlog = '/tmp/flask-skeleton-error.log'
