from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable

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


# Carousel items

class HomePageMainCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='main_carousel_items')
    tab_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=511)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video = models.URLField()
    call_to_action_url = models.URLField("Call to action URL", blank=True)
    call_to_action_caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('tab_title'),
        FieldPanel('title'),
        FieldPanel('summary'),
        ImageChooserPanel('image'),
        FieldPanel('video'),
        MultiFieldPanel([
            FieldPanel('call_to_action_url'),
            FieldPanel('call_to_action_caption')
        ], "Call To Action")
    ]


class HomePageSecondaryCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='secondary_carousel_items')
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    blockquote = models.CharField(max_length=511)
    author_name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author_job = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('blockquote'),
        FieldPanel('author_name'),
        FieldPanel('author_image'),
        FieldPanel('author_job'),
        FieldPanel('website')
    ]


# Homepage

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    secondary_carousel_introduction = models.CharField(max_length=511)

HomePage.content_panels = Page.content_panels + [
    InlinePanel(HomePage, 'main_carousel_items', label="Main carousel items"),
    InlinePanel(HomePage, 'secondary_carousel_items', label="Secondary carousel items"),
    FieldPanel('secondary_carousel_introduction'),
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
