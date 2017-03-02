flask-skeleton
--------------

flask-skeleton is a skeleton for using flask to develop apis service.
When you start a new flask api service, you can just clone it then develop base on it,
maybe there need you to modify some pathname settings.

You are not nessasary to care for the outermost layer's files, they are config files or scripts for deploying on my innernetwork server.
When you develop your api, you just need to focus in service directory. There has a ping demo, you can delete it.



### Features

- use [peewee](http://docs.peewee-orm.com/en/latest/) to ORM.

- use [python-decouple](https://github.com/henriquebastos/python-decouple/) to read environment variables settings.

- support [Sentry](https://docs.sentry.io/)

- detailed log



### Run

1. Create and activate a virtualenv

2. Install the requirements

3. create the .env file for decouple, the common envvars are in dotenv file, you need to write these vars in .env file, then use decouple to read them in settings.py uniformly.

4. run `python server.py`



### Plan：

1. Add new code must be readable for humans, code must pass the PEP8 checking, the files must be with utf8 encoding and without bomb header, use less try...except...

2. Put all the blueprint-routes under the routes directory, code in routes need as possible as simple, the business logic code don't write at here. If the route will connect database, must add the `pw_auto_manage_connect` decorator on it to make db connection be closed.

3. Put all business logic code in handlers directory, all of module's function in the handlers will auto add a decorator for log the function call detail, if you dont want to auto be added this decorator, you can add a `__nodeco__` attribute on the function.

4. Put all the defined model in models directory. Models default use MySQL connection, you can add new db connection in `modules.__ini__`. The connection generate by peewee's `connect()` way which read db_url from .env. (If you want PooledMySQLDataBase support RetryExceptionError, just set the db_url's scheme with `mysql+pool+retry`

5. Implement a function using the same name for route, handler and model, it let the code clean and tidy。

6. Use the log.py to log, it save log to diffrent file by DEFAULT_LOG_FILE, The error and normal log will be separated. And if log an Exception instance by error() or exception(), the log will send to sentry(if you set a sentry dns)

7. if not everyone has privileges to create table directly by model, so everytime you update db, must add the sql to schema.sql


### TODO：

- support statsd
- add unittest demo
- add flask-script

-----

- add feature arg when deploy
- rollback by feature arg
