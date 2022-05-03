from django.db import models

from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin
from wagtail_content_import.models import ContentImportMixin
from wagtailio.utils.mappers import StreamFieldMapper


class StandardPage(Page, ContentImportMixin, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    mapper_class = StreamFieldMapper

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )
