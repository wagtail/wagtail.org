from django.db import models

from wagtail.wagtailcore.models import Page

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from wagtail.wagtailsearch import index


from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)

# Homepage

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    pass

HomePage.content_panels = Page.content_panels + [
   
]

HomePage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Blog index

class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    pass

BlogIndexPage.content_panels = Page.content_panels + [
   
]

BlogIndexPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Blog page

class BlogPage(Page, SocialMediaMixin, CrossPageMixin):
    main_image = models.ForeignKey('images.WagtailIOImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    date = models.DateField()
    body = StreamField(StoryBlock())

BlogPage.content_panels = Page.content_panels + [
    ImageChooserPanel('main_image'),
    FieldPanel('date'),
    StreamFieldPanel('body')
]

BlogPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Standard content page

class StandardPage(Page, SocialMediaMixin, CrossPageMixin):
    main_image = models.ForeignKey('images.WagtailIOImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    body = StreamField(StoryBlock())

StandardPage.content_panels = Page.content_panels + [
    ImageChooserPanel('main_image'),
    StreamFieldPanel('body')
]

StandardPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
