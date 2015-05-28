from fabric.api import *

import uuid

STAGING_DB_USERNAME = "wagtailio"
DB_NAME = "wagtailio"
LOCAL_DUMP_PATH = "~/"
REMOTE_DUMP_PATH = "~/"

env.roledefs = {
    'production': ['wagtailio@by-web-4-a.torchbox.com', 'wagtailio@by-web-4-b.torchbox.com' ],
    'staging': ['wagtailio@by-staging-1.torchbox.com'],
}


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
    run('git pull origin staging')
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

@roles('staging')
def pull_staging_data():
    filename = "%s-%s.sql" % (DB_NAME, uuid.uuid4())
    local_path = "%s%s" % (LOCAL_DUMP_PATH, filename)
    remote_path = "%s%s" % (REMOTE_DUMP_PATH, filename)
    local_db_backup_path = "%svagrant-%s-%s.sql" % (LOCAL_DUMP_PATH, DB_NAME, uuid.uuid4())

    run('pg_dump -U%s -xOf %s' % (STAGING_DB_USERNAME, remote_path))
    run('gzip %s' % remote_path)
    get("%s.gz" % remote_path, "%s.gz" % local_path)
    run('rm %s.gz' % remote_path)

    local('pg_dump -xOf %s %s' % (local_db_backup_path, DB_NAME))
    puts('Previous local database backed up to %s' % local_db_backup_path)

    local('dropdb %s' % DB_NAME)
    local('createdb %s' % DB_NAME)
    local('gunzip %s.gz' % local_path)
    local('psql %s -f %s' % (DB_NAME, local_path))
    local('rm %s' % local_path)

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
