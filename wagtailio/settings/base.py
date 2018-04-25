"""
Django settings for wagtailio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
from os.path import abspath, dirname, join

import dj_database_url
import raven
from raven.exceptions import InvalidGitRepository


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()

# On Torchbox servers, many environment variables are prefixed with "CFG_"
for key, value in os.environ.items():
    if key.startswith('CFG_'):
        env[key[4:]] = value


# Absolute filesystem path to the Django project directory
PROJECT_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder
BASE_DIR = dirname(PROJECT_ROOT)

SECRET_KEY = env.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

APP_NAME = env.get('APP_NAME', 'wagtailio')


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'compressor',
    'taggit',
    'modelcluster',

    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.sites',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.contrib.redirects',
    'wagtail.contrib.forms',

    'wagtail.contrib.postgres_search',

    'wagtailio.utils',
    'wagtailio.core',
    'wagtailio.images',
    'wagtailio.standardpage',
    'wagtailio.newsletter',
    'wagtailio.developers',
    'wagtailio.blog',
    'wagtailio.features',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'wagtailio.urls'
WSGI_APPLICATION = 'wagtailio.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = env.get('STATIC_ROOT', join(BASE_DIR, 'static'))
STATIC_URL = env.get('STATIC_URL', '/static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files
MEDIA_ROOT = env.get('MEDIA_DIR', join(BASE_DIR, 'media'))
MEDIA_URL = env.get('MEDIA_URL', '/media/')


# S3 configuration

if 'AWS_STORAGE_BUCKET_NAME' in env:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    if 'AWS_S3_CUSTOM_DOMAIN' in env:
        AWS_S3_CUSTOM_DOMAIN = env['AWS_S3_CUSTOM_DOMAIN']

    INSTALLED_APPS += (
        'storages',
    )


# Database

if 'DATABASE_URL' in env:
    DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.get('PGDATABASE', APP_NAME),
            'CONN_MAX_AGE': 600,
            # User, host and port can be configured by the PGUSER, PGHOST and
            # PGPORT environment variables (these get picked up by libpq).
        }
    }


# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# Template configuration


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailio.context_processors.global_pages',
            ],
        },
    },
]


# Cache
# Use Redis or database as the cache backend

if 'REDIS_URL' in env:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env['REDIS_URL'],
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'database_cache',
        }
    }


# Email

if 'EMAIL_HOST' in env:
    EMAIL_HOST = env['EMAIL_HOST']

if 'EMAIL_PORT' in env:
    try:
        EMAIL_PORT = int(env['EMAIL_PORT'])
    except ValueError:
        pass

if 'EMAIL_HOST_USER' in env:
    EMAIL_HOST_USER = env['EMAIL_HOST_USER']

if 'EMAIL_HOST_PASSWORD' in env:
    EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']

if env.get('EMAIL_USE_TLS', 'false') == 'true':
    EMAIL_USE_TLS = True

if env.get('EMAIL_USE_SSL', 'false') == 'true':
    EMAIL_USE_SSL = True

if 'EMAIL_SUBJECT_PREFIX' in env:
    EMAIL_SUBJECT_PREFIX = env['EMAIL_SUBJECT_PREFIX']


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        'wagtailio': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Wagtail settings

WAGTAIL_SITE_NAME = "wagtailio"

WAGTAILIMAGES_IMAGE_MODEL = 'images.WagtailioImage'

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']


# Search

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.contrib.postgres_search.backend',
    },
}


# Sentry

if 'SENTRY_DSN' in env:
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    RAVEN_CONFIG = {
        'dsn': '{}?verify_ssl=0'.format(env['SENTRY_DSN']),
    }
    try:
        RAVEN_CONFIG['release'] = raven.fetch_git_sha(PROJECT_ROOT)  # noqa
    except InvalidGitRepository:
        try:
            RAVEN_CONFIG['release'] = env['GIT_REV']
        except KeyError:
            # Do not set the Sentry 'release' parameter
            pass
