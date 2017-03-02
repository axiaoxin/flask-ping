#!/usr/bin/env bash
proj_name=flask-skeleton
proj_root_path=/srv/$proj_name
proj_path=$proj_root_path/service
venv_path=/srv/.$proj_name-venv
zip_file=/srv/$proj_name.zip
backup_proj=/srv/$proj_name.`date '+%Y-%m-%d_%H:%M:%S'`
env_file=/srv/.env

if [ -f $zip_file ]; then
    ls | grep `date '+%Y-%m-%d' --date '30 days ago'` | xargs rm -rf
    mv $proj_root_path $backup_proj
    unp $zip_file && cp $env_file $proj_path
    . /srv/$venv_path/bin/activate
    pip install -r $proj_root_path/requirements.txt
    supervisorctl restart $proj_name && rm $zip_file
    curl localhost
else
    echo no $zip_file
fi
