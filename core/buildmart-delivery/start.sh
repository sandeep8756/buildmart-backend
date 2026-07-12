#!/bin/sh
set -e
cd /usr/src/app/buildmart-delivery
gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --workers 2 --bind 0.0.0.0:8003
