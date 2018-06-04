from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

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
    screenshot = models.ForeignKey(
        'images.WagtailIOImage',
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        InlinePanel('bullets', label="Bullets"),
        ImageChooserPanel('screenshot')
    ]


class FeaturePageFeatureAspect(Orderable, models.Model):
    page = ParentalKey('features.FeaturePage', related_name='feature_aspects')
    feature_aspect = models.ForeignKey(
        'features.FeatureAspect',
        models.CASCADE,
        related_name='+'
    )

    panels = [
        SnippetChooserPanel('feature_aspect')
    ]


class FeaturePage(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=255)

    @property
    def feature_index(self):
        return FeatureIndexPage.objects.ancestor_of(
            self
        ).order_by('-depth').first()

    @property
    def previous(self):
        if self.get_prev_sibling():
            return self.get_prev_sibling()
        else:
            return self.get_siblings().last()

    @property
    def next(self):
        if self.get_next_sibling():
            return self.get_next_sibling()
        else:
            return self.get_siblings().first()

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('feature_aspects', label="Feature Aspects")
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + \
        CrossPageMixin.panels


class FeatureIndexPageMenuOption(models.Model):
    page = ParentalKey('features.FeatureIndexPage',
                       related_name='secondary_menu_options')
    link = models.ForeignKey(
        'wagtailcore.Page',
        models.CASCADE,
        related_name='+'
    )
    label = models.CharField(max_length=255)

    panels = [
        PageChooserPanel('link'),
        FieldPanel('label')
    ]


class FeatureIndexPage(Page):
    introduction = models.CharField(max_length=255)

    @property
    def features(self):
        return FeaturePage.objects.live().child_of(self)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('secondary_menu_options', label="Secondary Menu Options")
    ]
