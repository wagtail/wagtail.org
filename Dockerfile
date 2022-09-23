# (Keep the version in sync with the node install below)
FROM node:18 as frontend

# Install front-end dependencies.
COPY package.json package-lock.json tsconfig.json webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files
COPY ./wagtailio/static/ ./wagtailio/static/
RUN npm run build:prod

# Build Python app.
FROM python:3.8-bullseye AS backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=wagtailio.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="--max-requests 1200 --access-logfile -"

# Install operating system dependencies.
RUN apt-get update -y && \
    apt-get install -y apt-transport-https rsync libmagickwand-dev unzip postgresql-client-13 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
EXPOSE 8000

# Create a non-root application user.
ARG UID=1000
RUN useradd wagtailio -u $UID -m
RUN chown -R wagtailio /app


FROM backend AS prod

# Switch to application user.
USER wagtailio

# Create a virtual environment
RUN python3 -m venv /home/wagtailio/venv
ENV PATH="/home/wagtailio/venv/bin:$PATH"
RUN pip install --upgrade pip wheel

# Install Gunicorn.
RUN pip install "gunicorn>=20.1,<20.2"

# Install production Python requirements.
COPY --chown=wagtailio requirements.txt /
RUN pip install -r /requirements.txt

COPY --chown=wagtailio --from=frontend ./wagtailio/static_compiled ./wagtailio/static_compiled

# Install application code.
COPY --chown=wagtailio . .

# Install assets
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Run application
CMD gunicorn wagtailio.wsgi:application


FROM backend AS dev

# Install Node.js because newer versions of Heroku CLI have a node binary dependency

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Install Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# Install AWS CLI
RUN curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip" && \
    unzip /tmp/awscli-bundle.zip -d /tmp && \
    /tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws && \
    rm /tmp/awscli-bundle.zip && rm -r /tmp/awscli-bundle

# Switch to application user.
USER wagtailio

# Pull in the node modules for the frontend
COPY --chown=wagtailio --from=frontend ./node_modules ./node_modules

# Install development Python requirements.
ENV PATH="/home/wagtailio/.local/bin:$PATH"
COPY --chown=wagtailio requirements.txt requirements-dev.txt /
RUN pip install -r /requirements-dev.txt
