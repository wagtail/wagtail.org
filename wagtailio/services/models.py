from django.db import models

from wagtail import blocks, fields
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from wagtailio.services.blocks import SectionBlock


class ServicesPage(Page):
    intro = models.TextField(null=True, blank=True)
    body = fields.StreamField(
        blocks.StreamBlock(
            [("section", SectionBlock())],
            min_num=4,
            max_num=4,
        ),
        blank=False,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]
