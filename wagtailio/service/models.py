from wagtail.core.models import Page
from wagtail_content_import.models import ContentImportMixin
from wagtailio.utils.models import SocialMediaMixin, CrossPageMixin


class ServicePage(Page, ContentImportMixin, SocialMediaMixin, CrossPageMixin):
    template = "service/services_page.html"

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )