"""
Django settings for wagtailio project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import contextlib
import os
from os.path import abspath, dirname, join
import sys

import dj_database_url


# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server

env = os.environ.copy()


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

INSTALLED_APPS = [
    "scout_apm.django",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",  # Must be before `django.contrib.staticfiles`
    "django.contrib.staticfiles",
    "taggit",
    "modelcluster",
    "rest_framework",
    "manifest_loader",
    "wagtail",
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
    "wagtail.api.v2",
    "wagtail.contrib.settings",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.search_promotions",
    "wagtailio.utils",
    "wagtailio.core",
    "wagtailio.images",
    "wagtailio.standardpage",
    "wagtailio.taxonomy",
    "wagtailio.search",
    "wagtailio.navigation",
    "wagtailio.newsletter",
    "wagtailio.blog",
    "wagtailio.features",
    "wagtailio.packages",
    "wagtailio.roadmap",
    "wagtailio.services",
    "wagtailio.showcase",
    "wagtailio.areweheadlessyet",
    "wagtailio.sitewide_alert",
    "wagtailmedia",
    "wagtail_newsletter",
    "pattern_library",
    "wagtailio.project_styleguide.apps.ProjectStyleguideConfig",
    "wagtailfontawesomesvg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
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

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = env.get("STATIC_ROOT", join(BASE_DIR, "static"))
STATIC_URL = env.get("STATIC_URL", "/static/")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (join(PROJECT_ROOT, "static_compiled"),)

# Place static files that need a specific URL (such as robots.txt and favicon.ico) in the "public" folder
WHITENOISE_ROOT = os.path.join(BASE_DIR, "public")

# Media files
MEDIA_ROOT = env.get("MEDIA_DIR", join(BASE_DIR, "media"))
MEDIA_URL = env.get("MEDIA_URL", "/media/")


# Basic auth settings
if env.get("BASIC_AUTH_ENABLED", "false").lower() == "true":
    MIDDLEWARE.insert(0, "baipw.middleware.BasicAuthIPWhitelistMiddleware")
    BASIC_AUTH_LOGIN = env.get("BASIC_AUTH_LOGIN", "wagtailorg")
    BASIC_AUTH_PASSWORD = env.get("BASIC_AUTH_PASSWORD", "showmewagtailorg")

    # Wagtail requires Authorization header to be present for the previews
    BASIC_AUTH_DISABLE_CONSUMING_AUTHORIZATION_HEADER = True

    # Paths that shouldn't be protected by basic auth
    if "BASIC_AUTH_WHITELISTED_PATHS" in env:
        BASIC_AUTH_WHITELISTED_PATHS = env["BASIC_AUTH_WHITELISTED_PATHS"].split(",")

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
    STORAGES["default"]["BACKEND"] = "storages.backends.s3.S3Storage"
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

    INSTALLED_APPS += ("storages",)


# Database

if "DATABASE_URL" in env:
    DATABASES = {"default": dj_database_url.config(conn_max_age=600)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.get("PGDATABASE", APP_NAME),
            "CONN_MAX_AGE": 600,
            # User, host and port can be configured by the PGUSER, PGHOST and
            # PGPORT environment variables (these get picked up by libpq).
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Template configuration


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "project_styleguide/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailio.context_processors.global_pages",
            ],
            "builtins": ["pattern_library.loader_tags"],
        },
    }
]


# Set s-max-age header that is used by reverse proxy/front end cache. See
# urls.py
with contextlib.suppress(ValueError):
    CACHE_CONTROL_S_MAXAGE = int(env.get("CACHE_CONTROL_S_MAXAGE", 600))


# Give front-end cache 30 second to revalidate the cache to avoid hitting the
# backend. See urls.py
CACHE_CONTROL_STALE_WHILE_REVALIDATE = int(
    env.get("CACHE_CONTROL_STALE_WHILE_REVALIDATE", 30)
)

SITEWIDE_ALERT_MAXAGE = int(env.get("SITEWIDE_ALERT_MAXAGE", 300))

SITEWIDE_ALERT_SMAXAGE = int(env.get("SITEWIDE_ALERT_SMAXAGE", 60 * 60 * 24 * 7))


# Cache
# Use Redis or database as the cache backend

# Prefer the TLS connection URL over non
REDIS_URL = env.get("REDIS_TLS_URL", env.get("REDIS_URL"))

if REDIS_URL:
    connection_pool_kwargs = {}

    if REDIS_URL.startswith("rediss"):
        # Heroku Redis uses self-signed certificates for secure redis conections.
        # https://stackoverflow.com/a/66286068
        # When using TLS, we need to disable certificate validation checks.
        connection_pool_kwargs["ssl_cert_reqs"] = None

    redis_options = {
        "IGNORE_EXCEPTIONS": True,
        "SOCKET_CONNECT_TIMEOUT": 2,  # seconds
        "SOCKET_TIMEOUT": 2,  # seconds
        "CONNECTION_POOL_KWARGS": connection_pool_kwargs,
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"{REDIS_URL}/0",
            "OPTIONS": redis_options,
        },
    }

    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
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
    with contextlib.suppress(ValueError):
        EMAIL_PORT = int(env["EMAIL_PORT"])

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

# Notification emails

WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = env.get(
    "MODERATION_NOTIFY_SUPERUSERS", False
)


# Security configuration
# https://docs.djangoproject.com/en/stable/ref/middleware/#module-django.middleware.security

# Force HTTPS redirect (enabled by default!)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True

# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# This is a setting activating the HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Since we are expecting our apps
# to run via TLS by default, this header is activated by default.
# The header can be deactivated by setting this setting to 0, as it is done in the
# dev and testing settings.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = DEFAULT_HSTS_SECONDS
if "SECURE_HSTS_SECONDS" in env:
    with contextlib.suppress(ValueError):
        SECURE_HSTS_SECONDS = int(env["SECURE_HSTS_SECONDS"])

# Do not use the `includeSubDomains` directive for HSTS. This needs to be prevented
# because the apps are running on client domains (or our own for staging), that are
# being used for other applications as well. We should therefore not impose any
# restrictions on these unrelated applications.
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True


# Content Security policy settings
# http://django-csp.readthedocs.io/en/latest/configuration.html
if "CSP_DEFAULT_SRC" in env:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

    CSP_INCLUDE_NONCE_IN = ["script-src", "style-src"]

    CSP_REPORT_ONLY = env.get("CSP_REPORT_ONLY", "false").lower() == "true"

    # The “special” source values of 'self', 'unsafe-inline', 'unsafe-eval', and 'none' must be quoted!
    # e.g.: CSP_DEFAULT_SRC = "'self'" Without quotes they will not work as intended.

    CSP_DEFAULT_SRC = env["CSP_DEFAULT_SRC"].split(",")
    if "CSP_SCRIPT_SRC" in env:
        CSP_SCRIPT_SRC = env["CSP_SCRIPT_SRC"].split(",")
    if "CSP_STYLE_SRC" in env:
        CSP_STYLE_SRC = env["CSP_STYLE_SRC"].split(",")
    if "CSP_IMG_SRC" in env:
        CSP_IMG_SRC = env["CSP_IMG_SRC"].split(",")
    if "CSP_MEDIA_SRC" in env:
        CSP_MEDIA_SRC = env["CSP_MEDIA_SRC"].split(",")
    if "CSP_CONNECT_SRC" in env:
        CSP_CONNECT_SRC = env["CSP_CONNECT_SRC"].split(",")
    if "CSP_FONT_SRC" in env:
        CSP_FONT_SRC = env["CSP_FONT_SRC"].split(",")
    if "CSP_BASE_URI" in env:
        CSP_BASE_URI = env["CSP_BASE_URI"].split(",")
    if "CSP_OBJECT_SRC" in env:
        CSP_OBJECT_SRC = env["CSP_OBJECT_SRC"].split(",")
    if "CSP_MANIFEST_SRC" in env:
        CSP_MANIFEST_SRC = env["CSP_MANIFEST_SRC"].split(",")
    if "CSP_REPORT_URI" in env:
        CSP_REPORT_URI = env["CSP_REPORT_URI"].split(",")


# Permissions policy settings
# Uses django-permissions-policy to return the header.
# https://github.com/adamchainz/django-permissions-policy
# The list of Chrome-supported features are in:
# https://github.com/w3c/webappsec-permissions-policy/blob/main/features.md
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "ambient-light-sensor": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "document-domain": [],
    "encrypted-media": [],
    "geolocation": [],
    "gyroscope": [],
    "interest-cohort": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "picture-in-picture": [],
    "usb": [],
}

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
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        }
    },
    "loggers": {
        "wagtailio": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


# Wagtail settings

WAGTAIL_SITE_NAME = "wagtail.org"

WAGTAILIMAGES_IMAGE_MODEL = "images.WagtailioImage"

WAGTAILIMAGES_EXTENSIONS = ["avif", "jpg", "png", "webp"]

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    "avif": "avif",
    "webp": "webp",
}

WILLOW_OPTIMIZERS = True

if "PRIMARY_HOST" in env:
    WAGTAILADMIN_BASE_URL = "https://{}".format(env["PRIMARY_HOST"])

# https://docs.wagtail.org/en/v2.8.1/releases/2.8.html#responsive-html-for-embeds-no-longer-added-by-default
WAGTAILEMBEDS_RESPONSIVE_HTML = True


# Search

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}


# Sentry configuration.
is_in_shell = len(sys.argv) > 1 and sys.argv[1] in ["shell", "shell_plus"]

if "SENTRY_DSN" in env and not is_in_shell:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.utils import get_default_release

    sentry_kwargs = {
        "dsn": env["SENTRY_DSN"],
        "integrations": [DjangoIntegration()],
    }

    # There's a chooser to toggle between environments at the top right corner on sentry.io
    # Values are typically 'staging' or 'production' but can be set to anything else if needed.
    # heroku config:set SENTRY_ENVIRONMENT=production
    if "SENTRY_ENVIRONMENT" in env:
        sentry_kwargs.update({"environment": env["SENTRY_ENVIRONMENT"]})

    release = get_default_release()
    if release is None:
        try:
            release = env["GIT_REV"]
        except KeyError:
            try:
                # Assume this is a Heroku-hosted app with the "runtime-dyno-metadata" lab enabled
                release = env["HEROKU_RELEASE_VERSION"]
            except KeyError:
                # If there's no commit hash, we do not set a specific release.
                release = None

    sentry_kwargs.update({"release": release})
    sentry_sdk.init(**sentry_kwargs)


# Favicon path
FAVICON_PATH = "img/favicons/favicon.ico"


# Frontend cache

if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in env:
    INSTALLED_APPS += ["wagtail.contrib.frontend_cache"]
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "EMAIL": env["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
            "TOKEN": env["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            "ZONEID": env["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }


MANIFEST_LOADER = {
    "output_dir": STATICFILES_DIRS[0],
}

PATTERN_LIBRARY_ENABLED = env.get("PATTERN_LIBRARY_ENABLED", "false").lower() == "true"

# Pattern library
PATTERN_LIBRARY = {
    # Groups of templates for the pattern library navigation. The keys
    # are the group titles and the values are lists of template name prefixes that will
    # be searched to populate the groups.
    "SECTIONS": (
        ("Style Guide", ["patterns/styleguide"]),
        ("Components", ["patterns/components"]),
        ("Pages", ["patterns/pages"]),
    ),
    # Configure which files to detect as templates.
    "TEMPLATE_SUFFIX": ".html",
    # Set which template components should be rendered inside of,
    # so they may use page-level component dependencies like CSS.
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
    # Any template in BASE_TEMPLATE_NAMES or any template that extends a template in
    # BASE_TEMPLATE_NAMES is a "page" and will be rendered as-is without being wrapped.
    "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
}

# GitHub integration
GITHUB_ROADMAP_ACCESS_TOKEN = env.get("GITHUB_ROADMAP_ACCESS_TOKEN", "")

# Mailchimp
if "MAILCHIMP_NEWSLETTER_ID" in env and "MAILCHIMP_ACCOUNT_ID" in env:
    MAILCHIMP_ACCOUNT_ID = env.get("MAILCHIMP_ACCOUNT_ID")
    MAILCHIMP_NEWSLETTER_ID = env.get("MAILCHIMP_NEWSLETTER_ID")

if all(
    _key in env
    for _key in [
        "WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY",
        "WAGTAIL_NEWSLETTER_FROM_NAME",
        "WAGTAIL_NEWSLETTER_REPLY_TO",
    ]
):
    WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY = env.get(
        "WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY"
    )
    WAGTAIL_NEWSLETTER_FROM_NAME = env.get("WAGTAIL_NEWSLETTER_FROM_NAME")
    WAGTAIL_NEWSLETTER_REPLY_TO = env.get("WAGTAIL_NEWSLETTER_REPLY_TO")

# all the tracking
FB_APP_ID = env.get("FB_APP_ID", "")
GOOGLE_TAG_MANAGER_ID = env.get("GOOGLE_TAG_MANAGER_ID", "")
