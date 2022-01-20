# Build Python app.
FROM python:3.8-buster AS backend

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
    apt-get install -y apt-transport-https rsync libmagickwand-dev unzip postgresql-client-13 && \
    rm -rf /var/lib/apt/lists/*

# Don't use the root user.
ARG UID=1000
RUN useradd wagtailio -u $UID

# Install Gunicorn.
RUN pip install "gunicorn>=20.1,<20.2"


FROM backend AS prod

# Install production Python requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install application code.
COPY . .

RUN chown -R wagtailio .
USER wagtailio

# Install assets
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Compress
RUN SECRET_KEY=none django-admin compress

# Run application
CMD gunicorn wagtailio.wsgi:application


FROM backend AS dev

# Install Heroku CLI
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install AWS CLI
RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip"
RUN unzip /tmp/awscli-bundle.zip -d /tmp
RUN /tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

# Install development Python requirements.
COPY requirements.txt /
COPY requirements-dev.txt /
RUN pip install -r /requirements-dev.txt
