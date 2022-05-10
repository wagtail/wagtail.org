import requests
from django.conf import settings
from wagtail.core.signals import page_published, page_unpublished

from .models import AreWeHeadlessYetHomePage, AreWeHeadlessYetTopicPage


def register_signal_handlers():
    deploy_url = getattr(settings, "VERCEL_DEPLOY_HOOK_URL", None)
    if not deploy_url:
        return

    from .thread_pool import run_in_thread_pool

    @run_in_thread_pool
    def deploy(sender, **kwargs):
        """Triggers a build on Vercel."""

        try:
            requests.post(deploy_url, timeout=settings.VERCEL_DEPLOY_REQUEST_TIMEOUT)
        except requests.exceptions.Timeout:
            pass  # Ignore this error

    page_published.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_published.connect(deploy, sender=AreWeHeadlessYetTopicPage)

    page_unpublished.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_unpublished.connect(deploy, sender=AreWeHeadlessYetTopicPage)
