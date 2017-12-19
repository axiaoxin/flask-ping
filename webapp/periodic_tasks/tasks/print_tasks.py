from app import app


@app.task
def print_arg(arg):
    print arg


@app.task
def print_args(*args):
    print args
