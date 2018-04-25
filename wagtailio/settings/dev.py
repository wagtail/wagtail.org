from .base import *


DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

SECRET_KEY = '7nn(g(lb*8!r_+cc3m8bjxm#xu!q)6fidwgg&$p$6a+alm+eex'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FB_APP_ID = 0

try:
    from .local import *
except ImportError:
    pass
