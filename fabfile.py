from fabric.api import *


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
