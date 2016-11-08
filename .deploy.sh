#!/bin/bash
proj_name=flask-ping
proj_root_path=/srv/$proj_name
proj_path=$proj_root_path/service
zip_file=/srv/$proj_name.zip
backup_proj=/srv/old.$proj_name
env_file=/srv/.env

if [ -f $zip_file ]; then
    rm -rf $backup_proj; mv $proj_root_path $backup_proj
    unp $zip_file && cp $env_file $proj_path
    supervisorctl restart $proj_name && rm $zip_file
    curl localhost
else
    echo no $zip_file
fi
