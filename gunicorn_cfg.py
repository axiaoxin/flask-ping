from multiprocessing import cpu_count

proc_name = 'flask-skeleton'
bind = '127.0.0.1:5000'
workers = cpu_count() * 2 + 1
worker_class = 'gevent'
reload = True
pidfile = '/var/run/flask-skeleton.pid'
raw_env = []
pythonpath = '/srv/flask-skeleton/service'
accesslog = '/data/log/flask-skeleton/gunicorn.acc.log'
access_log_format = '%(t)s %(h)s %(s)s "%(r)s" %(b)s "%(f)s" "%(a)s" "%({Header}i)s"'
errorlog = '/data/log/flask-skeleton/gunicorn.err.log'
