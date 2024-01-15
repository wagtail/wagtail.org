from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control


def get_default_cache_control_kwargs():
    s_maxage = getattr(settings, "CACHE_CONTROL_S_MAXAGE", None)
    stale_while_revalidate = getattr(
        settings, "CACHE_CONTROL_STALE_WHILE_REVALIDATE", None
    )
    cache_control_kwargs = {
        "s_maxage": s_maxage,
        "stale_while_revalidate": stale_while_revalidate,
        "public": True,
    }
    return {k: v for k, v in cache_control_kwargs.items() if v is not None}


def get_default_cache_control_decorator():
    cache_control_kwargs = get_default_cache_control_kwargs()
    return cache_control(**cache_control_kwargs)


def get_default_cache_control_method_decorator(original_method):
    @method_decorator(get_default_cache_control_decorator())
    def decorated_method(self, *args, **kwargs):
        return original_method(self, *args, **kwargs)

    return decorated_method
