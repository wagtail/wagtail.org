from .base import *  # noqa: F403


# Do not force HTTP->HTTPS redirect when running the production setup on localhost
SECURE_SSL_REDIRECT = False

# Use the default (non-manifest) staticfiles storage in tests so they don't require compiled front-end assets to be present
STORAGES = {
    **STORAGES,  # noqa: F405
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
