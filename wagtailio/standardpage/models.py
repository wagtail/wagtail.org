from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class StandardPage(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        StreamFieldPanel('body')
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + \
        CrossPageMixin.panels
