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
    if key.startswith("CFG_"):
        env[key[4:]] = value


# Absolute filesystem path to the Django project directory
PROJECT_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder
BASE_DIR = dirname(PROJECT_ROOT)

SECRET_KEY = env.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if "ALLOWED_HOSTS" in env:
    ALLOWED_HOSTS = env["ALLOWED_HOSTS"].split(",")

APP_NAME = env.get("APP_NAME", "wagtailio")


# Application definition

INSTALLED_APPS = (
    "scout_apm.django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "compressor",
    "taggit",
    "modelcluster",
    "wagtail_transfer",
    "wagtail_airtable",
    "wagtail.core",
    "wagtail_image_import",
    "wagtail_content_import",
    "wagtail_content_import.pickers.google",
    "wagtail_content_import.pickers.local",
    "wagtail.admin",
    "wagtail.documents",
    "wagtail.snippets",
    "wagtail.users",
    "wagtail.sites",
    "wagtail.images",
    "wagtail.embeds",
    "wagtail.search",
    "wagtail.contrib.redirects",
    "wagtail.contrib.forms",
    "wagtail.contrib.postgres_search",
    "wagtailio.utils",
    "wagtailio.core",
    "wagtailio.images",
    "wagtailio.standardpage",
    "wagtailio.newsletter",
    "wagtailio.service",
    "wagtailio.developers",
    "wagtailio.blog",
    "wagtailio.features",
    "wagtailaltgenerator",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "wagtailio.urls"
WSGI_APPLICATION = "wagtailio.wsgi.application"


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = env.get("STATIC_ROOT", join(BASE_DIR, "static"))
STATIC_URL = env.get("STATIC_URL", "/static/")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATICFILES_DIRS = (join(PROJECT_ROOT, "static"),)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_ROOT = env.get("MEDIA_DIR", join(BASE_DIR, "media"))
MEDIA_URL = env.get("MEDIA_URL", "/media/")


# Basic auth settings
if os.environ.get("BASIC_AUTH_ENABLED", "false").lower() == "true":
    MIDDLEWARE.insert(0, "baipw.middleware.BasicAuthIPWhitelistMiddleware")
    BASIC_AUTH_LOGIN = "wagtailio"
    BASIC_AUTH_PASSWORD = "showmewagtailio"
    BASIC_AUTH_WHITELISTED_IP_NETWORKS = [
        "78.32.251.192/28",
        "89.197.53.244/30",
        "193.227.244.0/23",
        "2001:41c8:103::/48",
    ]
    if "BASIC_AUTH_WHITELISTED_HTTP_HOSTS" in env:
        BASIC_AUTH_WHITELISTED_HTTP_HOSTS = env[
            "BASIC_AUTH_WHITELISTED_HTTP_HOSTS"
        ].split(",")


# S3 configuration

if "AWS_STORAGE_BUCKET_NAME" in env:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_STORAGE_BUCKET_NAME = env["AWS_STORAGE_BUCKET_NAME"]
    AWS_S3_FILE_OVERWRITE = False

    # Disables signing every single file.
    AWS_QUERYSTRING_AUTH = False

    # You need this to enable signing files. Some old regions may have use a
    # different version than v4.
    AWS_S3_SIGNATURE_VERSION = env.get("AWS_S3_SIGNATURE_VERSION", "s3v4")

    # Set individual files to be private and only allow access to them via
    # bucket policy.
    AWS_DEFAULT_ACL = "private"

    if "AWS_S3_ENDPOINT_URL" in env:
        # This setting is required for signing.
        # Please use endpoint from
        # https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region
        # e.g. "https://s3.eu-west-2.amazonaws.com"
        AWS_S3_ENDPOINT_URL = env["AWS_S3_ENDPOINT_URL"]

    if "AWS_S3_REGION_NAME" in env:
        # This setting is required for signing.
        AWS_S3_REGION_NAME = env["AWS_S3_REGION_NAME"]

    if "AWS_S3_CUSTOM_DOMAIN" in env:
        AWS_S3_CUSTOM_DOMAIN = env["AWS_S3_CUSTOM_DOMAIN"]

    if "AWS_S3_SECURE_URLS" in env:
        AWS_S3_SECURE_URLS = env["AWS_S3_SECURE_URLS"].strip().lower() == "true"

    INSTALLED_APPS += ("storages",)


# Database

if "DATABASE_URL" in env:
    DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env.get("PGDATABASE", APP_NAME),
            "CONN_MAX_AGE": 600,
            # User, host and port can be configured by the PGUSER, PGHOST and
            # PGPORT environment variables (these get picked up by libpq).
        }
    }


# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)


# Template configuration


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [join(PROJECT_ROOT, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtailio.context_processors.global_pages",
            ]
        },
    }
]


# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py
try:
    CACHE_CONTROL_S_MAXAGE = int(env.get("CACHE_CONTROL_S_MAXAGE", 600))
except ValueError:
    pass


# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)


# Cache
# Use Redis or database as the cache backend

if "REDIS_URL" in env:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env["REDIS_URL"],
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "database_cache",
        }
    }


# Email

if "EMAIL_HOST" in env:
    EMAIL_HOST = env["EMAIL_HOST"]

if "EMAIL_PORT" in env:
    try:
        EMAIL_PORT = int(env["EMAIL_PORT"])
    except ValueError:
        pass

if "EMAIL_HOST_USER" in env:
    EMAIL_HOST_USER = env["EMAIL_HOST_USER"]

if "EMAIL_HOST_PASSWORD" in env:
    EMAIL_HOST_PASSWORD = env["EMAIL_HOST_PASSWORD"]

if env.get("EMAIL_USE_TLS", "false") == "true":
    EMAIL_USE_TLS = True

if env.get("EMAIL_USE_SSL", "false") == "true":
    EMAIL_USE_SSL = True

if "EMAIL_SUBJECT_PREFIX" in env:
    EMAIL_SUBJECT_PREFIX = env["EMAIL_SUBJECT_PREFIX"]

if "SERVER_EMAIL" in env:
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = env["SERVER_EMAIL"]


# Security configuration
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

if env.get("SECURE_SSL_REDIRECT", "true").strip().lower() == "true":
    SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if "SECURE_HSTS_SECONDS" in env:
    try:
        SECURE_HSTS_SECONDS = int(env["SECURE_HSTS_SECONDS"])
    except ValueError:
        pass

if env.get("SECURE_BROWSER_XSS_FILTER", "true").lower().strip() == "true":
    SECURE_BROWSER_XSS_FILTER = True

if env.get("SECURE_CONTENT_TYPE_NOSNIFF", "true").lower().strip() == "true":
    SECURE_CONTENT_TYPE_NOSNIFF = True


# Referrer-policy header settings
# https://django-referrer-policy.readthedocs.io/en/1.0/

REFERRER_POLICY = env.get(
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
        "sentry": {
            "level": "ERROR",
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "wagtailio": {
            "handlers": ["console", "sentry", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console", "sentry", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "sentry", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["mail_admins", "sentry", "console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


# Wagtail settings

WAGTAIL_SITE_NAME = "wagtailio"

WAGTAILIMAGES_IMAGE_MODEL = "images.WagtailioImage"

if "PRIMARY_HOST" in env:
    BASE_URL = "http://%s/" % env["PRIMARY_HOST"]
    
# https://docs.wagtail.io/en/v2.8.1/releases/2.8.html#responsive-html-for-embeds-no-longer-added-by-default
WAGTAILEMBEDS_RESPONSIVE_HTML = True


# Search

WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.contrib.postgres_search.backend"}
}


# Sentry

if "SENTRY_DSN" in env:
    INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
    RAVEN_CONFIG = {"dsn": env["SENTRY_DSN"]}
    try:
        RAVEN_CONFIG["release"] = raven.fetch_git_sha(PROJECT_ROOT)  # noqa
    except InvalidGitRepository:
        try:
            RAVEN_CONFIG["release"] = env["GIT_REV"]
        except KeyError:
            # Do not set the Sentry 'release' parameter
            pass

# Favicon path
FAVICON_PATH = "img/favicons/favicon.ico"


# Frontend cache

if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
    INSTALLED_APPS += ("wagtail.contrib.frontend_cache",)  # noqa
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
            "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

WAGTAILCONTENTIMPORT_DOCX_PARSER = "wagtailio.utils.parsers.DocxHTMLParser"
WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY = env.get(
    "WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY"
)
WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG = env.get(
    "WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG"
)

WAGTAILIMAGEIMPORT_GOOGLE_PICKER_API_KEY = env.get(
    "WAGTAILCONTENTIMPORT_GOOGLE_PICKER_API_KEY"
)
WAGTAILIMAGEIMPORT_GOOGLE_OAUTH_CLIENT_SECRET = env.get(
    "WAGTAILCONTENTIMPORT_GOOGLE_OAUTH_CLIENT_CONFIG"
)

WAGTAILIMAGEIMPORT_FIELD_MAPPING = {
    "id": "driveidmapping__drive_id", 
    "name": "title",
    "imageMediaMetadata__time": "exif_datetime",
    "md5Checksum": "md5_hash"
}


AIRTABLE_API_KEY = env.get(
    "AIRTABLE_API_KEY"
)
BLOG_AIRTABLE_BASE_KEY = env.get(
    "BLOG_AIRTABLE_BASE_KEY"
)
BLOG_AIRTABLE_URL = env.get(
    "BLOG_AIRTABLE_URL"
)
FEATURES_AIRTABLE_BASE_KEY = env.get(
    "FEATURES_AIRTABLE_BASE_KEY"
)
FEATURES_AIRTABLE_URL = env.get(
    "FEATURES_AIRTABLE_URL"
)
WAGTAIL_AIRTABLE_ENABLED = all((AIRTABLE_API_KEY, BLOG_AIRTABLE_BASE_KEY, BLOG_AIRTABLE_URL, FEATURES_AIRTABLE_BASE_KEY, FEATURES_AIRTABLE_URL))
AIRTABLE_IMPORT_SETTINGS = {
    'blog.BlogPage': {
        'AIRTABLE_BASE_KEY': BLOG_AIRTABLE_BASE_KEY,
        'AIRTABLE_TABLE_NAME': 'Posts',
        'AIRTABLE_UNIQUE_IDENTIFIER': {
            'ID': 'id',
        },
        'AIRTABLE_SERIALIZER': 'wagtailio.blog.serializers.BlogPageSerializer',
        'AIRTABLE_BASE_URL': BLOG_AIRTABLE_URL,
    },
    'features.FeatureDescription': {
        'AIRTABLE_BASE_KEY': FEATURES_AIRTABLE_BASE_KEY,
        'AIRTABLE_TABLE_NAME': 'Feature Descriptions',
        'AIRTABLE_UNIQUE_IDENTIFIER': {
            'ID': 'id',
        },
        'AIRTABLE_SERIALIZER': 'wagtailio.features.serializers.FeatureDescriptionSerializer',
        'AIRTABLE_BASE_URL': FEATURES_AIRTABLE_URL,
    },
}

WAGTAILTRANSFER_CONNECTED_INSTANCE_NAME = env.get(
    "WAGTAILTRANSFER_CONNECTED_INSTANCE_NAME"
)
WAGTAILTRANSFER_CONNECTED_INSTANCE_BASE_URL = env.get(
    "WAGTAILTRANSFER_CONNECTED_INSTANCE_BASE_URL"
)
WAGTAILTRANSFER_CONNECTED_INSTANCE_SECRET_KEY = env.get(
    "WAGTAILTRANSFER_CONNECTED_INSTANCE_SECRET_KEY"
)

WAGTAILTRANSFER_SOURCES = {
    WAGTAILTRANSFER_CONNECTED_INSTANCE_NAME: {
        'BASE_URL': WAGTAILTRANSFER_CONNECTED_INSTANCE_BASE_URL,
        'SECRET_KEY': WAGTAILTRANSFER_CONNECTED_INSTANCE_SECRET_KEY,
    },
} if all((WAGTAILTRANSFER_CONNECTED_INSTANCE_NAME, WAGTAILTRANSFER_CONNECTED_INSTANCE_BASE_URL, WAGTAILTRANSFER_CONNECTED_INSTANCE_SECRET_KEY)) else {}

WAGTAILTRANSFER_SECRET_KEY = env.get(
    "WAGTAILTRANSFER_SECRET_KEY"
)

WAGTAILTRANSFER_UPDATE_RELATED_MODELS = ['images.wagtailioimage', 'features.featureaspect', 'features.featuredescription']
