from .base import *  # noqa
from .base import env


# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

FB_APP_ID = 710333029076622


# Basic configuration

if env.get('SECURE_SSL_REDIRECT', 'true') == 'true':
    SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# enable HSTS only once the site is working properly on https with
# the actual live domain name
# SECURE_HSTS_SECONDS = 31536000  # 1 year


try:
    from .local import *  # noqa
except ImportError:
    pass
