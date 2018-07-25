#!/bin/bash

if [ -d "logs" ]
then
    echo "Log folder already created!"
else
    mkdir logs
fi

if [ "$PYTHONENV" = "production" ]
then
    gunicorn -b 0.0.0.0:8000 --workers 8 --access-logformat "Remote client - %({X-Forwarded-For}i)s Web Server - %(h)s %(r)s %(s)s"  --access-logfile logs/nubitoic.log --error-logfile logs/nubitoic.err.log wsgi:app
else
    python wsgi.py
fi