#!/bin/sh

echo "##############################################"
echo "#             LAUNCH GUNICORN                #"
echo "##############################################"
cd /app
gunicorn index:app --error-logfile "/var/log/gunicorn/error.log" --access-logfile "/var/log/gunicorn/access.log" --capture-output --timeout 90 --bind=0.0.0.0:5000