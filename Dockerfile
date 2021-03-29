# Build Python app.
FROM python:3.8-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=wagtailio.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -"

EXPOSE 8000

# Install operating system dependencies.
RUN apt-get update -y && \
    apt-get install -y apt-transport-https rsync libmagickwand-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Gunicorn.
RUN pip install "gunicorn>=19.8,<19.9"

# Install Python requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install application code.
COPY . .

# Don't use the root user.
RUN useradd wagtailio
RUN chown -R wagtailio .
USER wagtailio

# Install assets
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Compress
RUN SECRET_KEY=none django-admin compress

# Run application
CMD gunicorn wagtailio.wsgi:application
