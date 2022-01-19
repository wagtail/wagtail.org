from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class AreWeHeadlessYetHomePage(Page, SocialMediaMixin, CrossPageMixin):
    THUMBS_UP = "thumbs up"
    THUMBS_DOWN = "thumbs down"
    ICON_CHOICES = [
        (THUMBS_UP, THUMBS_UP),
        (THUMBS_DOWN, THUMBS_DOWN),
    ]
    strapline_icon = models.CharField(
        max_length=255,
        choices=ICON_CHOICES,
        default=THUMBS_UP,
    )
    strapline_text = RichTextField(features=["bold", "italic"])

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("strapline_icon"),
                FieldPanel("strapline_text"),
            ],
            "strapline",
        ),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
