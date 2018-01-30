from celery_main import celery_app, logger
from utils.cache import get_redislock

@celery_app.task
def print_arg(arg):
    lock = get_redislock('print_arg:%s' % arg, blocking_timeout=1)
    if lock.acquire():
        logger.info('print %s' %arg)
        import time
        time.sleep(3)
        lock.release()
        return arg
    else:
        logger.warning('blocking')


@celery_app.task
def print_args(*args):
    logger.info('print %s' % args)
    return args
