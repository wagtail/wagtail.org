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

COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.CSSMinFilter",
    ]
}

COMPUTER_VISION_API_KEY = env.get('COMPUTER_VISION_API_KEY')
COMPUTER_VISION_REGION = env.get('COMPUTER_VISION_REGION')
ALT_GENERATOR_MAX_TAGS = env.get("ALT_GENERATOR_MAX_TAGS", 5)
ALT_GENERATOR_MIN_CONFIDENCE = env.get("ALT_GENERATOR_MIN_CONFIDENCE", 40)

WAGTAIL_AB_TESTING_WORKER_TOKEN = env.get("WAGTAIL_AB_TESTING_WORKER_TOKEN", None)

FB_APP_ID = 710333029076622


try:
    from .local import *  # noqa
except ImportError:
    pass
