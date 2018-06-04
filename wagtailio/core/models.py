from django.db import models
from django.shortcuts import redirect

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    PageChooserPanel, StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)


# Carousel items

class HomePageMainCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='main_carousel_items')
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=511)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    video = models.URLField()
    call_to_action_internal_link = models.ForeignKey(
        'wagtailcore.Page',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    call_to_action_external_link = models.URLField("Call to action URL", blank=True)
    call_to_action_caption = models.CharField(max_length=255, blank=True)

    @property
    def call_to_action_link(self):
        if self.call_to_action_internal_link:
            return self.call_to_action_internal_link.url
        else:
            return self.call_to_action_external_link

    panels = [
        FieldPanel('title'),
        FieldPanel('summary'),
        ImageChooserPanel('image'),
        FieldPanel('video'),
        MultiFieldPanel([
            PageChooserPanel('call_to_action_internal_link'),
            FieldPanel('call_to_action_external_link'),
            FieldPanel('call_to_action_caption')
        ], "Call To Action")
    ]


class HomePageSecondaryCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='secondary_carousel_items')
    title = models.CharField(max_length=255)
    desktop_image = models.ForeignKey(
        'images.WagtailIOImage',
        models.CASCADE,
        related_name='+'
    )
    mobile_image = models.ForeignKey(
        'images.WagtailIOImage',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    blockquote = models.TextField()
    author_name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'images.WagtailIOImage',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    author_job = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('desktop_image'),
        ImageChooserPanel('mobile_image'),
        FieldPanel('blockquote'),
        FieldPanel('author_name'),
        ImageChooserPanel('author_image'),
        FieldPanel('author_job'),
        FieldPanel('website')
    ]


# Homepage

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    secondary_carousel_introduction = models.CharField(max_length=511)

    content_panels = Page.content_panels + [
        InlinePanel('main_carousel_items', label="Main carousel items"),
        FieldPanel('secondary_carousel_introduction'),
        InlinePanel('secondary_carousel_items', label="Secondary carousel items"),
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels

# New Homepage

class HomePageNew(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        StreamFieldPanel('body')
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
