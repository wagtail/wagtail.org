import urllib

from django.conf import settings


def global_pages(request):
    return {
        "WAGTAILADMIN_BASE_URL": getattr(settings, "WAGTAILADMIN_BASE_URL", ""),
        "DEBUG": getattr(settings, "DEBUG", ""),
        "FB_APP_ID": getattr(settings, "FB_APP_ID", ""),
    }
