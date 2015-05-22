from operator import attrgetter

from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

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
    call_to_action_internal_link = models.ForeignKey(
        'wagtailcore.Page',
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
        FieldPanel('tab_title'),
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
        'images.WagtailIOImage',
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
        ImageChooserPanel('author_image'),
        FieldPanel('author_job'),
        FieldPanel('website')
    ]


# Homepage

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    secondary_carousel_introduction = models.CharField(max_length=511)

HomePage.content_panels = Page.content_panels + [
    InlinePanel(HomePage, 'main_carousel_items', label="Main carousel items"),
    FieldPanel('secondary_carousel_introduction'),
    InlinePanel(HomePage, 'secondary_carousel_items', label="Secondary carousel items"),
]

HomePage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Blog index

class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    pass

BlogIndexPage.content_panels = Page.content_panels + [

]

BlogIndexPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Blog page

class Author(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        ImageChooserPanel('image'),
        FieldPanel('url')
    ]

register_snippet(Author)


class BlogPage(Page, SocialMediaMixin, CrossPageMixin):
    author = models.ForeignKey(
        'core.Author',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    main_image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField()
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    @property
    def siblings(self):
        siblings = self.get_siblings(
            inclusive=False
        ).type(self.__class__)
        siblings = [sibling.specific for sibling in siblings]
        return sorted(siblings, key=attrgetter('date'), reverse=True)

BlogPage.content_panels = Page.content_panels + [
    SnippetChooserPanel('author', Author),
    ImageChooserPanel('main_image'),
    FieldPanel('date'),
    FieldPanel('introduction'),
    StreamFieldPanel('body')
]

BlogPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Standard content page

class StandardPage(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

StandardPage.content_panels = Page.content_panels + [
    StreamFieldPanel('body')
]

StandardPage.promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels


# Feature page

class Bullet(Orderable, models.Model):
    snippet = ParentalKey('core.FeatureAspect', related_name='bullets')
    title = models.CharField(max_length=255)
    text = RichTextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('text')
    ]


class FeatureAspect(ClusterableModel):
    title = models.CharField(max_length=255)
    screenshot = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.title

FeatureAspect.panels = [
    FieldPanel('title'),
    InlinePanel(FeatureAspect, 'bullets', label="Bullets"),
    ImageChooserPanel('screenshot')
]

register_snippet(FeatureAspect)


class FeaturePageFeatureAspect(Orderable, models.Model):
    page = ParentalKey('core.FeaturePage', related_name='feature_aspects')
    feature_aspect = models.ForeignKey('core.FeatureAspect', related_name='+')

    panels = [
        SnippetChooserPanel('feature_aspect', FeatureAspect)
    ]


class FeaturePage(Page):
    introduction = models.CharField(max_length=255)

FeaturePage.content_panels = Page.content_panels + [
    FieldPanel('introduction'),
    InlinePanel(FeaturePage, 'feature_aspects', label="Feature Aspects")
]
