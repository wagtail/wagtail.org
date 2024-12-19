from concurrent.futures import ThreadPoolExecutor
import logging

from django.conf import settings

import requests


logger = logging.getLogger("wagtailio")


def run_thread_pool():
    max_workers = settings.VERCEL_DEPLOY_MAX_WORKERS
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            func, args, kwargs = yield
            executor.submit(func, *args, **kwargs)


thread_pool = run_thread_pool()

# Advance the coroutine to the first yield (priming)
next(thread_pool)


def run_in_thread_pool(function):
    """
    Cheap aysnc, see https://stackoverflow.com/a/54432426
    """

    def decorator(*args, **kwargs):
        thread_pool.send((function, args, kwargs))

    return decorator


@run_in_thread_pool
def deploy(sender, **kwargs):
    """Triggers a build on Vercel."""

    try:
        logger.info("Triggering build on Vercel.")
        response = requests.post(
            settings.VERCEL_DEPLOY_HOOK_URL,
            timeout=settings.VERCEL_DEPLOY_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        logger.info("Build triggered on Vercel.")

    except requests.exceptions.Timeout:
        logger.warning("The request to trigger a new build on Vercel has timed out.")
        return  # Ignore this error

    except (KeyboardInterrupt, SystemExit):
        raise

    except Exception:
        logger.exception("The request to trigger a new build on Vercel has failed.")
