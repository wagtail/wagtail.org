from fabric import colors
from fabric.api import local, prompt, task
from fabric.context_managers import warn_only


PRODUCTION_APP_INSTANCE = 'wagtailio-production'
STAGING_APP_INSTANCE = 'wagtailio-staging'

LOCAL_MEDIA_FOLDER = './media'
LOCAL_DATABASE_NAME = 'wagtailio'


############
# Production
############

@task
def pull_production_media():
    pull_media_from_s3_heroku(PRODUCTION_APP_INSTANCE)


@task
def push_production_media():
    push_media_to_s3_heroku(PRODUCTION_APP_INSTANCE)


@task
def pull_production_data():
    pull_database_from_heroku(PRODUCTION_APP_INSTANCE)


@task
def push_production_data():
    push_database_to_heroku(PRODUCTION_APP_INSTANCE)


@task
def deploy_production():
    deploy_to_heroku(PRODUCTION_APP_INSTANCE, local_branch='main',
                     remote_branch='master')


@task
def production_shell():
    open_heroku_shell(PRODUCTION_APP_INSTANCE)


#########
# Staging
#########


@task
def pull_staging_media():
    pull_media_from_s3_heroku(STAGING_APP_INSTANCE)


@task
def push_staging_media():
    push_media_to_s3_heroku(STAGING_APP_INSTANCE)


@task
def pull_staging_data():
    pull_database_from_heroku(STAGING_APP_INSTANCE)


@task
def push_staging_data():
    push_database_to_heroku(STAGING_APP_INSTANCE)


@task
def deploy_staging():
    deploy_to_heroku(STAGING_APP_INSTANCE, local_branch='staging',
                     remote_branch='master')


@task
def staging_shell():
    open_heroku_shell(STAGING_APP_INSTANCE)


#######
# Local
#######


def clean_local_database(local_database_name=LOCAL_DATABASE_NAME):
    local(
        'sudo -u postgres psql  -d {database_name} -c "DROP SCHEMA public '
        'CASCADE; CREATE SCHEMA public;"'.format(
            database_name=local_database_name
        )
    )


def delete_local_database(local_database_name=LOCAL_DATABASE_NAME):
    with warn_only():
        local('dropdb {database_name}'.format(database_name=LOCAL_DATABASE_NAME))


def deploy_prompt(app_instance):
    prompt_msg = 'You are about to do a manual deployment. \nPlease type ' \
                 'the application name "{app_instance}" in order to ' \
                 'proceed:\n>>> '.format(app_instance=colors.red(app_instance,
                                                                 bold=True))
    prompt(prompt_msg, validate=app_instance)


########
# Heroku
########


def check_heroku_authenticated():
    """
    Call before running any methods that capture output of the heroku command, such as get_heroku_variable.

    This ensures that the user is prompted to log in if they are not currently authenticated.
    """
    with warn_only():
        result = local('heroku auth:whoami', capture=True)

    if result.return_code != 0:
        local('heroku auth:login')


def get_heroku_variable(app_instance, variable):
    return local('heroku config:get {var} --app {app}'.format(
        app=app_instance,
        var=variable,
    ), capture=True).strip()


def pull_media_from_s3_heroku(app_instance):
    check_heroku_authenticated()

    aws_access_key_id = get_heroku_variable(app_instance, 'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_heroku_variable(app_instance,
                                                'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_heroku_variable(app_instance,
                                                  'AWS_STORAGE_BUCKET_NAME')
    pull_media_from_s3(aws_access_key_id, aws_secret_access_key,
                       aws_storage_bucket_name)


def push_media_to_s3_heroku(app_instance):
    prompt_msg = 'You are about to push your media folder contents to the ' \
                 'S3 bucket. It\'s a destructive operation. \n' \
                 'Please type the application name "{app_instance}" to ' \
                 'proceed:\n>>> '.format(app_instance=colors.red(app_instance,
                                                                 bold=True))
    prompt(prompt_msg, validate=app_instance)

    check_heroku_authenticated()

    aws_access_key_id = get_heroku_variable(app_instance, 'AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_heroku_variable(app_instance,
                                                'AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name = get_heroku_variable(app_instance,
                                                  'AWS_STORAGE_BUCKET_NAME')
    push_media_to_s3(aws_access_key_id, aws_secret_access_key,
                     aws_storage_bucket_name)


def pull_database_from_heroku(app_instance):
    delete_local_database()
    local('heroku pg:pull --app {app} DATABASE_URL {local_database}'.format(
        app=app_instance,
        local_database=LOCAL_DATABASE_NAME
    ))
    local('django-admin createcachetable')


def push_database_to_heroku(app_instance):
    prompt_msg = 'You are about to push your local database to Heroku. ' \
                 'It\'s a destructive operation and will override the ' \
                 'database on the server. \n' \
                 'Please type the application name "{app_instance}" to ' \
                 'proceed:\n>>> '.format(app_instance=colors.red(app_instance,
                                                                 bold=True))
    prompt(prompt_msg, validate=app_instance)
    local('heroku maintenance:on --app {app}'.format(app=app_instance))
    local('heroku ps:stop --app {app} web'.format(app=app_instance))
    local('heroku pg:backups:capture --app {app}'.format(app=app_instance))
    local('heroku pg:reset --app {app}'.format(app=app_instance))
    local('heroku pg:push --app {app} {localdb} DATABASE_URL'.format(
        app=app_instance,
        localdb=LOCAL_DATABASE_NAME,
    ))
    local('heroku ps:restart --app {app}'.format(app=app_instance))
    local('heroku maintenance:off --app {app}'.format(app=app_instance))


def setup_heroku_git_remote(app_instance):
    remote_name = 'heroku-{app}'.format(app=app_instance)
    local('heroku git:remote --app {app} --remote {remote}'.format(
        app=app_instance, remote=remote_name
    ))
    return remote_name


def deploy_to_heroku(app_instance, local_branch='master',
                     remote_branch='master'):
    print(
        'This will push your local "{local_branch}" branch to remote '
        '"{remote_branch}" branch.'.format(
            local_branch=local_branch,
            remote_branch=remote_branch
        )
    )
    deploy_prompt(app_instance)
    remote_name = setup_heroku_git_remote(app_instance)
    local('git push {remote} {local_branch}:{remote_branch}'.format(
        remote=remote_name,
        local_branch=local_branch,
        remote_branch=remote_branch,
    ))


def open_heroku_shell(app_instance, shell_command='bash'):
    local('heroku run --app {app} {command}'.format(
        app=app_instance,
        command=shell_command,
    ))


####
# S3
####


def aws(command, aws_access_key_id, aws_secret_access_key, **kwargs):
    return local(
        'AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_key} '
        'aws {command}'.format(
            access_key_id=aws_access_key_id,
            secret_key=aws_secret_access_key,
            command=command,
        ),
        **kwargs
    )


def pull_media_from_s3(aws_access_key_id, aws_secret_access_key,
                       aws_storage_bucket_name,
                       local_media_folder=LOCAL_MEDIA_FOLDER):
    aws_cmd = 's3 sync --delete s3://{bucket_name} {local_media}'.format(
        bucket_name=aws_storage_bucket_name,
        local_media=local_media_folder,
    )
    aws(aws_cmd, aws_access_key_id, aws_secret_access_key)


def push_media_to_s3(aws_access_key_id, aws_secret_access_key,
                     aws_storage_bucket_name,
                     local_media_folder=LOCAL_MEDIA_FOLDER):
    aws_cmd = 's3 sync --delete {local_media} s3://{bucket_name}/'.format(
        bucket_name=aws_storage_bucket_name,
        local_media=local_media_folder,
    )
    aws(aws_cmd, aws_access_key_id, aws_secret_access_key)
