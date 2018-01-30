from celery_main import celery_app

@celery_app.task
def print_arg(arg):
    print arg


@celery_app.task
def print_args(*args):
    print args
