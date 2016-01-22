import getpass
import warnings
from datetime import datetime
from fabric.api import *

import uuid

STAGING_DB_USERNAME = "wagtailio"
DB_NAME = "wagtailio"
LOCAL_DUMP_PATH = "~/"
REMOTE_DUMP_PATH = "~/"

env.roledefs = {
    'production': ['wagtailio@web-1-a.rslon.torchbox.net', 'wagtailio@web-1-b.rslon.torchbox.net' ],
    'staging': ['wagtailio@by-staging-1.torchbox.com'],
}


@roles('production')
def deploy_production():
    if getpass.getuser() == 'toby':
        warnings.warn("USER IS TOBY")
    run('git pull origin')
    run('pip install -r requirements.txt')
    run('django-admin migrate --noinput')
    run('django-admin collectstatic --noinput')
    run('django-admin compress')
    run('django-admin update_index')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


@roles('staging')
def deploy_staging():
    if getpass.getuser() == 'toby':
        warnings.warn("USER IS TOBY")
    run('git pull origin')
    run('pip install -r requirements.txt')
    run('django-admin migrate --noinput')
    run('django-admin collectstatic --noinput')
    run('django-admin compress')
    run('django-admin update_index')
    run('cacheclear')
    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


@roles('staging')
def createsuperuser_staging():
    run('django-admin createsuperuser')


@roles('production')
def deploy_production():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    run('git pull origin master')
    run('pip install -r requirements.txt')
    run('django-admin migrate --noinput')
    run('django-admin collectstatic --noinput')
    run('django-admin compress')
    run('django-admin update_index')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


@roles('staging')
def deploy_staging():
    # Remove this line when you're happy that this task is correct
    raise RuntimeError("Please check the fabfile before using it")

    run('git pull origin staging')
    run('pip install -r requirements.txt')
    run('django-admin migrate --noinput')
    run('django-admin collectstatic --noinput')
    run('django-admin compress')
    run('django-admin update_index')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')


def _pull_data(env_name, remote_db_name, local_db_name, remote_dump_path, local_dump_path):
    timestamp = datetime.now().strftime('%Y%m%d-%I%M%S')

    filename = '.'.join([env_name, remote_db_name, timestamp, 'sql'])
    remote_filename = remote_dump_path + filename
    local_filename = local_dump_path + filename

    params = {
        'remote_db_name': remote_db_name,
        'remote_filename': remote_filename,
        'local_db_name': local_db_name,
        'local_filename': local_filename,
    }

    # Dump/download database from server
    run('pg_dump {remote_db_name} -xOf {remote_filename}'.format(**params))
    run('gzip {remote_filename}'.format(**params))
    get('{remote_filename}.gz'.format(**params), '{local_filename}.gz'.format(**params))
    run('rm {remote_filename}.gz'.format(**params))

    # Load database locally
    local('gunzip {local_filename}.gz'.format(**params))
    local('dropdb {local_db_name}'.format(**params))
    local('createdb {local_db_name}'.format(**params))
    local('psql {local_db_name} -f {local_filename}'.format(**params))
    local('rm {local_filename}'.format(**params))


@roles('production')
def pull_production_data():
    _pull_data(
        env_name='production',
        remote_db_name='wagtailio',
        local_db_name='wagtailio',
        remote_dump_path='/usr/local/django/wagtailio/tmp/',
        local_dump_path='/tmp/',
    )


@roles('staging')
def pull_staging_data():
    _pull_data(
        env_name='staging',
        remote_db_name='wagtailio',
        local_db_name='wagtailio',
        remote_dump_path='/usr/local/django/wagtailio/tmp/',
        local_dump_path='/tmp/',
    )


@roles('staging')
def pull_staging_media():
    media_filename = "wagtailio-%s-media.tar.gz" % uuid.uuid4()
    local_media_dump = "%s%s" % (LOCAL_DUMP_PATH, media_filename)
    remote_media_dump = "%s%s" % (REMOTE_DUMP_PATH, media_filename)

    with cd('/usr/local/django/wagtailio'):
        run('tar cvf - media | gzip -1 >%s' % remote_media_dump)

    get('%s' % remote_media_dump, '%s' % local_media_dump)

    local('rm -rf media.old')
    local('mv media media.old || true')
    local('gzip -dc %s | tar xvf -' % local_media_dump)
    local('rm -f %s' % local_media_dump)
    run('rm -f %s' % remote_media_dump)
