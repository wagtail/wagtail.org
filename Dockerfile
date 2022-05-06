# We use Debian images because they are considered more stable than the alpine
# ones becase they use a different C compiler. Debian images also come with
# all useful packages required for image manipulation out of the box. They
# however weight a lot, approx. up to 1.5GiB per built image.
FROM python:3.8 as production

ARG POETRY_HOME=/opt/poetry
ARG POETRY_INSTALL_ARGS="--no-dev"

# IMPORTANT: Remember to review both of these when upgrading
ARG POETRY_VERSION=1.1.13
# To get this value locally:
# $ wget https://raw.githubusercontent.com/python-poetry/poetry/1.1.13/get-poetry.py
# $ sha1sum get-poetry.py
ARG POETRY_INSTALLER_SHA=eedf0fe5a31e5bb899efa581cbe4df59af02ea5f

# Install dependencies in a virtualenv
ENV VIRTUAL_ENV=/venv

RUN useradd wagtailio --create-home && mkdir /app $VIRTUAL_ENV && chown -R wagtailio /app $VIRTUAL_ENV

WORKDIR /app

# Set default environment variables. They are used at build time and runtime.
# If you specify your own environment variables on Heroku or Dokku, they will
# override the ones set here. The ones below serve as sane defaults only.
#  * PATH - Make sure that Poetry is on the PATH, along with our venv
#  * PYTHONUNBUFFERED - This is useful so Python does not hold any messages
#    from being output.
#    https://docs.python.org/3.9/using/cmdline.html#envvar-PYTHONUNBUFFERED
#    https://docs.python.org/3.9/using/cmdline.html#cmdoption-u
#  * DJANGO_SETTINGS_MODULE - default settings used in the container.
#  * PORT - default port used. Please match with EXPOSE so it works on Dokku.
#    Heroku will ignore EXPOSE and only set PORT variable. PORT variable is
#    read/used by Gunicorn.
#  * WEB_CONCURRENCY - number of workers used by Gunicorn. The variable is
#    read by Gunicorn.
#  * GUNICORN_CMD_ARGS - additional arguments to be passed to Gunicorn. This
#    variable is read by Gunicorn
ENV PATH=${POETRY_HOME}/bin:$VIRTUAL_ENV/bin:$PATH \
    POETRY_INSTALL_ARGS=${POETRY_INSTALL_ARGS} \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=wagtailio.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3 \
    GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --max-requests-jitter 50 --access-logfile - --timeout 25"

# Make $BUILD_ENV available at runtime
ARG BUILD_ENV
ENV BUILD_ENV=${BUILD_ENV}

# Port exposed by this container. Should default to the port used by your WSGI
# server (Gunicorn). This is read by Dokku only. Heroku will ignore this.
EXPOSE 8000

# Install poetry using the installer (keeps Poetry's dependencies isolated from the app's)
# chown protects us against cases where files downloaded by poetry have invalid ownership
# (see https://git.torchbox.com/internal/wagtail-kit/-/merge_requests/682)
# chmod ensures poetry dependencies are accessible when packages are installed
RUN wget https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/get-poetry.py && \
    echo "${POETRY_INSTALLER_SHA} get-poetry.py" | sha1sum -c - && \
    python get-poetry.py && \
    rm get-poetry.py && \
    chown -R root:root ${POETRY_HOME} && \
    chmod -R 0755 ${POETRY_HOME}

# Don't use the root user as it's an anti-pattern and Heroku does not run
# containers as root either.
# https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime
USER wagtailio

# Install your app's Python requirements.
RUN python -m venv $VIRTUAL_ENV
COPY --chown=wagtailio pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && poetry install ${POETRY_INSTALL_ARGS} --no-root --extras gunicorn

# Copy application code.
COPY --chown=wagtailio . .

# Run poetry install again to install our project (so the the wagtailio package is always importable)
RUN poetry install ${POETRY_INSTALL_ARGS}

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

# Load shortcuts
COPY ./docker/bashrc.sh /home/wagtailio/.bashrc

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn wagtailio.wsgi:application

# These steps won't be run on production
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root

# Install `psql`, useful for `manage.py dbshell`
RUN apt-get update && apt-get install -y postgresql-client

# Restore user
# I found this will remove required permissions when developing in gitpod.
# USER wagtailio

# do nothing forever - exec commands elsewhere
CMD tail -f /dev/null
