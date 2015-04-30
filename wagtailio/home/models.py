from django.db import models

from wagtail.wagtailcore.models import Page

from utils.blocks import StoryBlock
from utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    pass


HomePage.content_panels = Page.content_panels + [
   
]

HomePage.promote_panels = Page.promote_panels + [
   
] + SocialMediaMixin.panels + CrossPageMixin.panels