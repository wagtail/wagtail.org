from concurrent.futures import ThreadPoolExecutor

from django.conf import settings


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
