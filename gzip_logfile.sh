#! /usr/bin/env bash

log_path="/var/log/flask_api"
yesterday=`date -d '-1 day' +%Y%m%d`

mv $log_path/app.log $log_path/app.$yesterday.log
mv $log_path/gunicorn.log $log_path/gunicorn.$yesterday.log
mv $log_path/crontab.log $log_path/crontab.$yesterday.log
mv $log_path/supervisor.log $log_path/supervisor.$yesterday.log

gzip $log_path/app.$yesterday.log
gzip $log_path/gunicorn.$yesterday.log
gzip $log_path/crontab.$yesterday.log
gzip $log_path/supervisor.$yesterday.log
