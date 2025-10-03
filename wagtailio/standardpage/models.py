from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtail_ai.panels import AIFieldPanel
from wagtail_ai.prompts import DefaultPrompt

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class StandardPage(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    content_panels = Page.content_panels + [
        AIFieldPanel(
            "introduction",
            prompts=[DefaultPrompt.DESCRIPTION],
        ),
        FieldPanel("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]
