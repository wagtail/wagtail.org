from .base import *  # noqa: F403


# Debugging to be enabled locally only
DEBUG = True

# This key to be used locally only.
SECRET_KEY = "not-a-secret"  # noqa: S105

# Display sent emails in the console while developing locally.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use dummy app ID for development
FB_APP_ID = 0

# Do not force HTTP->HTTPS redirect when running the production setup on localhost
SECURE_SSL_REDIRECT = False

# Enable FE component library
PATTERN_LIBRARY_ENABLED = True
ALLOWED_HOSTS = ["*"]

# Mailchimp
MAILCHIMP_ACCOUNT_ID = "Fake"
MAILCHIMP_NEWSLETTER_ID = "Fake"

# Load django-extensions only in dev
INSTALLED_APPS += ["django_extensions"]  # noqa: F405


with contextlib.suppress(ImportError):  # noqa: F405
    from .local import *  # noqa: F403
