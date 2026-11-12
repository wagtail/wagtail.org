from .base import *  # noqa: F403


# Do not force HTTP->HTTPS redirect when running the production setup on localhost
SECURE_SSL_REDIRECT = False

# Static files aren't collected for tests, so don't look them up in a manifest.
STORAGES["staticfiles"]["BACKEND"] = (  # noqa: F405
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)
