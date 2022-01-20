from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page

from wagtailio.areweheadlessyet.blocks import HomePageBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class AreWeHeadlessYetHomePage(Page, SocialMediaMixin, CrossPageMixin):
    THUMBS_UP = "thumbs up"
    THUMBS_DOWN = "thumbs down"
    ICON_CHOICES = [
        (THUMBS_UP, THUMBS_UP),
        (THUMBS_DOWN, THUMBS_DOWN),
    ]
    strapline_icon = models.CharField(
        max_length=15,
        choices=ICON_CHOICES,
        default=THUMBS_UP,
    )
    strapline_text = RichTextField(features=["bold", "italic"])
    body = StreamField(HomePageBlock())

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("strapline_icon"),
                FieldPanel("strapline_text"),
            ],
            "strapline",
        ),
        StreamFieldPanel("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    # Set this so that this page type can only be created under the root page.
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []

    # Ensure that only one page of this type can be created.
    max_count = 1
