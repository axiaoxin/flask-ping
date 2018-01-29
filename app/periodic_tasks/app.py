from celery import Celery


app = Celery('tasks')
app.config_from_object('config')


if __name__ == '__main__':
    app.start()
