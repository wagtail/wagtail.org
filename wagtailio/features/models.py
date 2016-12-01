from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    StreamFieldPanel)
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from wagtailio.features.blocks import FeatureIndexPageBlock
from wagtailio.utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)


class Bullet(Orderable, models.Model):
    snippet = ParentalKey('features.FeatureAspect', related_name='bullets')
    title = models.CharField(max_length=255)
    text = RichTextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('text')
    ]


@register_snippet
class FeatureAspect(ClusterableModel):
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True)
    screenshot = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        InlinePanel('bullets', label="Bullets"),
        ImageChooserPanel('screenshot'),
        FieldPanel('video_url'),
    ]


class FeatureDescriptionFeatureAspect(Orderable, models.Model):
    page = ParentalKey('features.FeatureDescription', related_name='feature_aspects')
    feature_aspect = models.ForeignKey('features.FeatureAspect', related_name='+')

    panels = [
        SnippetChooserPanel('feature_aspect')
    ]


@register_snippet
class FeatureDescription(ClusterableModel):
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255, blank=True)
    documentation_link = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        FieldPanel('introduction'),
        FieldPanel('documentation_link'),
        InlinePanel('feature_aspects', label="Feature Aspects"),
    ]


class FeatureIndexPage(Page):
    body = StreamField(FeatureIndexPageBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
