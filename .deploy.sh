#!/bin/bash

if [ -f "biz_checkup_web_service.zip" ]; then
    rm -rf /srv/old.biz_checkup_web_service && mv /srv/biz_checkup_web_service /srv/old.biz_checkup_web_service
    unp /srv/biz_checkup_web_service.zip && cp /srv/.env /srv/biz_checkup_web_service/service
    supervisorctl restart flask_api && rm /srv/biz_checkup_web_service.zip
    curl localhost
else
    echo 'no biz_checkup_web_service.zip'
fi
