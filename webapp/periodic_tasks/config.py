from celery.schedules import crontab

broker_url = 'redis://'

result_backend = 'redis://'

timezone = 'Asia/Shanghai'

imports = [
    'tasks.print_tasks',
]

beat_schedule = {
    'print-arg-every-1-seconds': {
        'task': 'tasks.print_tasks.print_arg',
        'schedule': 1,
        'args': ('hello', )
    },
    'print-args-every-1-minutes': {
        'task': 'tasks.print_tasks.print_args',
        'schedule': crontab(minute='*/1'),
        'args': ('world', )
    },
}
