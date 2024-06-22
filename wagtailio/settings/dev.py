from .base import *  # noqa

# Debugging to be enabled locally only
DEBUG = True

# This key to be used locally only.
SECRET_KEY = "7nn(g(lb*8!r_+cc3m8bjxm#xu!q)6fidwgg&$p$6a+alm+eex"

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


try:
    from .local import *  # noqa
except ImportError:
    pass
