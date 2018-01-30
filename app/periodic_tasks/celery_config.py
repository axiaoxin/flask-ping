from celery.schedules import crontab
from decouple import config

broker_url = config('BROKER_URL', default='redis://localhost:6379/1')

result_backend = config('RESULT_BACKEND', default='redis://localhost:6379/1')

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
