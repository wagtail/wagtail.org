from .base import *  # noqa: F403


# Debugging to be enabled locally only
DEBUG = True

# REST API v3 preview, for local demo purposes only
INSTALLED_APPS += ["wagtail.api.v3"]  # noqa: F405

# This key to be used locally only.
SECRET_KEY = "not-a-secret"  # noqa: S105

# Display sent emails in the console while developing locally.
MAILERS["default"]["BACKEND"] = "django.core.mail.backends.console.EmailBackend"  # noqa: F405

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


with contextlib.suppress(ImportError):  # noqa: F405
    from .local import *  # noqa: F403
