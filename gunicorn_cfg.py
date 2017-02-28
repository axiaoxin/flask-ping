from multiprocessing import cpu_count

proc_name = 'flask-ping'
bind = '127.0.0.1:1111'
workers = cpu_count() * 2 + 1
worker_class = 'gevent'
reload = True
pidfile = '/var/run/flask-ping.pid'
raw_env = []
pythonpath = '/srv/flask-ping/service'
accesslog = '/data/log/flask-ping/gunicorn.acc.log'
access_log_format = '%(t)s %(h)s %(s)s "%(r)s" "%(f)s" "%(a)s" "%({Header}i)s"'
errorlog = '/data/log/flask-ping/gunicorn.err.log'

