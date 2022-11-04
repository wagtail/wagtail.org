from .base import *  # noqa
from .base import env

COMPUTER_VISION_API_KEY = env.get("COMPUTER_VISION_API_KEY")
COMPUTER_VISION_REGION = env.get("COMPUTER_VISION_REGION")
ALT_GENERATOR_MAX_TAGS = env.get("ALT_GENERATOR_MAX_TAGS", 5)
ALT_GENERATOR_MIN_CONFIDENCE = env.get("ALT_GENERATOR_MIN_CONFIDENCE", 40)

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


try:
    from .local import *  # noqa
except ImportError:
    pass
