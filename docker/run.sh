#!/bin/sh
set -e

# If PORT is not set, default to 8000.

if [ -z $PORT ];
then
    export PORT=8000
fi

# If web concurrency is not set, default to 2 workers.
# Reference:
# http://docs.gunicorn.org/en/stable/settings.html#worker-processes
if [ -z $WEB_CONCURRENCY ];
then
    export WEB_CONCURRENCY=2
fi

# Run migrations after deployment.
django-admin createcachetable || true
django-admin migrate || true
django-admin update_index || true
django-admin compress || true

# Start gunicorn.
exec gunicorn wagtailio.wsgi:application
