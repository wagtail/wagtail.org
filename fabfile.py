from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task

PRODUCTION_APP_INSTANCE = "wagtailio-production"
STAGING_APP_INSTANCE = "wagtailio-staging"

LOCAL_MEDIA_FOLDER = "/vagrant/media"
LOCAL_IMAGES_FOLDER = "/vagrant/media/original_images"
LOCAL_DATABASE_NAME = "wagtailio"


############
# Production
############


@task
def pull_production_media(c):
    """Pull media from production AWS S3"""
    pull_media_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_data(c):
    """Pull database from production Heroku Postgres"""
    pull_database_from_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def production_shell(c):
    """Spin up a one-time Heroku production dyno and connect to shell"""
    open_heroku_shell(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_images(c):
    """Pull images from production AWS S3"""
    pull_images_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


#########
# Staging
#########


@task
def pull_staging_media(c):
    """Pull media from staging AWS S3"""
    pull_media_from_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_data(c):
    """Pull database from staging Heroku Postgres"""
    pull_database_from_heroku(c, STAGING_APP_INSTANCE)


@task
def staging_shell(c):
    """Spin up a one-time Heroku staging dyno and connect to shell"""
    open_heroku_shell(c, STAGING_APP_INSTANCE)


@task
def push_staging_media(c):
    """Push local media content to staging isntance"""
    push_media_to_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_images(c):
    """Pull images from staging AWS S3"""
    pull_images_from_s3_heroku(c, STAGING_APP_INSTANCE)


#######
# Local
#######


def delete_local_database(c, local_database_name=LOCAL_DATABASE_NAME):
    local(
        "dropdb --if-exists {database_name}".format(database_name=LOCAL_DATABASE_NAME)
    )


########
# Heroku
########


def check_if_logged_in_to_heroku(c):
    if not local("heroku auth:whoami", warn=True):
        raise Exit(
            'Log-in with the "heroku login -i" command before running this ' "command."
        )


def check_if_heroku_app_access_granted(c, app_instance):
    check_if_logged_in_to_heroku(c)
    # Any command targeting an app would do. This one prints the list of who has access.
    error = local(f"heroku access --app {app_instance}", hide="both", warn=True).stderr
    if error:
        raise Exit(
            "You do not have access to this app. Please either try to add yourself with:\n"
            f"heroku apps:join --app {app_instance}\n\n"
            "Or ask a team admin to add you with:\n"
            f"heroku access:add <your email address> --app {app_instance}"
        )


def get_heroku_variable(c, app_instance, variable):
    check_if_logged_in_to_heroku(c)
    return local(
        "heroku config:get {var} --app {app}".format(app=app_instance, var=variable)
    ).stdout.strip()


def pull_media_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def pull_database_from_heroku(c, app_instance):
    check_if_heroku_app_access_granted(c, app_instance)
    delete_local_database(c)
    local(
        "heroku pg:pull --app {app} DATABASE_URL {local_database}".format(
            app=app_instance, local_database=LOCAL_DATABASE_NAME
        )
    )
    answer = (
        input(
            "Any superuser accounts you previously created locally will"
            " have been wiped. Do you wish to create a new superuser? (Y/n): "
        )
        .strip()
        .lower()
    )
    if not answer or answer == "y":
        local("django-admin createsuperuser", pty=True)


def open_heroku_shell(c, app_instance, shell_command="bash"):
    check_if_logged_in_to_heroku(c)
    local(
        "heroku run --app {app} {command}".format(
            app=app_instance, command=shell_command
        )
    )


####
# S3
####


def aws(c, command, aws_access_key_id, aws_secret_access_key, **kwargs):
    return local(
        "AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_key} "
        "aws {command}".format(
            access_key_id=aws_access_key_id,
            secret_key=aws_secret_access_key,
            command=command,
        ),
        **kwargs,
    )


def pull_media_from_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
):
    aws_cmd = "s3 sync --delete s3://{bucket_name} {local_media}".format(
        bucket_name=aws_storage_bucket_name, local_media=local_media_folder
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def push_media_to_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    prompt_msg = (
        "You are about to push your media folder contents to the "
        "S3 bucket. It's a destructive operation. \n"
        'Please type the application name "{app_instance}" to '
        "proceed:\n>>> ".format(app_instance=make_bold(app_instance))
    )
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    push_media_to_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def push_media_to_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
):
    aws_cmd = "s3 sync --delete {local_media} s3://{bucket_name}/".format(
        bucket_name=aws_storage_bucket_name, local_media=local_media_folder
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def pull_images_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "AWS_STORAGE_BUCKET_NAME"
    )
    pull_images_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def pull_images_from_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_images_folder=LOCAL_IMAGES_FOLDER,
):
    aws_cmd = "s3 sync --delete s3://{bucket_name}/original_images {local_media}".format(
        bucket_name=aws_storage_bucket_name, local_media=local_images_folder
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)
    # The above command just syncs the original images, so we need to drop the wagtailimages_renditions
    # table so that the renditions will be re-created when requested on the local build.
    delete_local_renditions()


def delete_local_renditions(local_database_name=LOCAL_DATABASE_NAME):
    try:
        local(
            'sudo -u postgres psql  -d {database_name} -c "DELETE FROM images_rendition;"'.format(
                database_name=local_database_name
            )
        )
    except:
        pass

    try:
        local(
            'sudo -u postgres psql  -d {database_name} -c "DELETE FROM wagtailimages_rendition;"'.format(
                database_name=local_database_name
            )
        )
    except:
        pass


def make_bold(msg):
    return "\033[1m{}\033[0m".format(msg)
