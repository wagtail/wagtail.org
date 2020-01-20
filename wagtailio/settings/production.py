from .base import *  # noqa
from .base import env


# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

# Use local cache for Django compressor so we can build it in Docker
CACHES["compressor_cache"] = {  # noqa
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
}
COMPRESS_CACHE_BACKEND = "compressor_cache"

COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]

FB_APP_ID = 710333029076622


try:
    from .local import *  # noqa
except ImportError:
    pass
