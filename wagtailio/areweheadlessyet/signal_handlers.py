from django.conf import settings

from wagtail.signals import page_published, page_unpublished

from .models import AreWeHeadlessYetHomePage, AreWeHeadlessYetTopicPage


def register_signal_handlers():
    if not getattr(settings, "VERCEL_DEPLOY_HOOK_URL", None):
        return

    from .thread_pool import deploy

    page_published.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_published.connect(deploy, sender=AreWeHeadlessYetTopicPage)

    page_unpublished.connect(deploy, sender=AreWeHeadlessYetHomePage)
    page_unpublished.connect(deploy, sender=AreWeHeadlessYetTopicPage)
