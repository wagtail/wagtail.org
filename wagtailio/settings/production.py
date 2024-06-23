from .base import *  # noqa
from .base import env

VERCEL_DEPLOY_HOOK_URL = env.get("VERCEL_DEPLOY_HOOK_URL", None)
try:
    VERCEL_DEPLOY_REQUEST_TIMEOUT = int(env.get("VERCEL_DEPLOY_REQUEST_TIMEOUT", 1))
except ValueError:
    VERCEL_DEPLOY_REQUEST_TIMEOUT = 1

try:
    VERCEL_DEPLOY_MAX_WORKERS = int(env.get("VERCEL_DEPLOY_MAX_WORKERS", 10))
except ValueError:
    VERCEL_DEPLOY_MAX_WORKERS = 10

MANIFEST_LOADER["cache"] = True  # noqa

# Use secure cookies for the session and CSRF cookies.
# If these are set to True, the cookies will be marked as “secure”, which means
# browsers may ensure that the cookies are only sent under an HTTPS connection.
# https://docs.djangoproject.com/en/4.1/ref/settings/#session-cookie-secure
# https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-cookie-secure
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

try:
    from .local import *  # noqa
except ImportError:
    pass
