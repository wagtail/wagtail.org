from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class AreWeHeadlessYetHomePage(Page):
    THUMBS_UP = "\U0001f44D"
    THUMBS_DOWN = "\U0001f44E"
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

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []
