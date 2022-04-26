from threading import Thread

import requests
from django.conf import settings
from wagtail.core.signals import page_published, page_unpublished

from .models import AreWeHeadlessYetHomePage, AreWeHeadlessYetTopicPage


def postpone(function):
    """
    Cheap aysnc, see https://stackoverflow.com/a/28913218
    """

    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


@postpone
def deploy(sender, **kwargs):
    """Triggers a build on Vercel."""

    response = requests.post(settings.VERCEL_DEPLOY_HOOK_URL)
    response.raise_for_status()


def register_signal_handlers():
    if not getattr(settings, "VERCEL_DEPLOY_HOOK_URL", None):
        return

    page_published.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_published.connect(deploy, sender=AreWeHeadlessYetTopicPage)

    page_unpublished.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_unpublished.connect(deploy, sender=AreWeHeadlessYetTopicPage)
