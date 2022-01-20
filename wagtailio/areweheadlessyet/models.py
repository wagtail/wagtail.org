from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page

from wagtailio.areweheadlessyet.blocks import HomePageBlock


class AreWeHeadlessYetHomePage(Page):
    THUMBS_UP = "\U0001f44D"
    THUMBS_DOWN = "\U0001f44E"
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

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
