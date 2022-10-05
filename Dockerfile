# (Keep the version in sync with the node install below)
FROM node:18 as frontend

# Install front-end dependencies.
COPY package.json package-lock.json tsconfig.json webpack.config.js ./
RUN npm ci --no-optional --no-audit --progress=false

# Compile static files
COPY ./wagtailio/static/ ./wagtailio/static/
RUN npm run build:prod


# Build Python app - this stage is a common base for the prod and dev stages
FROM python:3.8-bullseye AS backend

ARG POETRY_VERSION=1.2.1

ENV DJANGO_SETTINGS_MODULE=wagtailio.settings.production \
    GUNICORN_CMD_ARGS="--max-requests 1200 --max-requests-jitter 50 --access-logfile -" \
    PATH=/home/wagtailio/.local/bin:/venv/bin:$PATH \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv \
    WEB_CONCURRENCY=3

# Install operating system dependencies.
RUN apt-get update -y && \
    apt-get install -y apt-transport-https rsync libmagickwand-dev unzip postgresql-client-13 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
EXPOSE 8000

# Create a virtual environment and install Poetry
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip wheel \
    && /usr/local/bin/python -m pip install poetry==$POETRY_VERSION

# Create a non-root application user.
ARG UID=1000 GID=1000
RUN groupadd --gid $GID --force wagtailio \
    && useradd --create-home --uid $UID -g wagtailio wagtailio
RUN chown --recursive $UID:$GID /app /venv


# This stage builds the image that will run in production
FROM backend AS prod

# Switch to application user
USER wagtailio

# Install production dependencies
COPY --chown=wagtailio pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Copy in application code and install the root package
COPY --chown=wagtailio . .
RUN poetry install --only-root

# Collect static files
COPY --chown=wagtailio --from=frontend ./wagtailio/static_compiled ./wagtailio/static_compiled
RUN SECRET_KEY=none django-admin collectstatic --noinput --clear

# Run application
CMD gunicorn wagtailio.wsgi:application


# This stage builds the image that we use for development
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

# Switch to the application user
USER wagtailio

# Install development dependencies
COPY --chown=wagtailio pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Pull in the node modules for the frontend
COPY --chown=wagtailio --from=frontend ./node_modules ./node_modules

# Make sure the working directory is on PYTHONPATH (so django-admin etc. can
# import wagtailio)
ENV PYTHONPATH=/app
