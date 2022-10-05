from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtailio.core.blocks import StandaloneCTABlock
from wagtailio.features.blocks import FeatureIndexBlock


class Bullet(Orderable, models.Model):
    snippet = ParentalKey("features.FeatureAspect", related_name="bullets")
    title = models.CharField(max_length=255)
    text = RichTextField()

    panels = [FieldPanel("title"), FieldPanel("text")]


@register_snippet
class FeatureAspect(ClusterableModel):
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True)
    screenshot = models.ForeignKey(
        "images.WagtailIOImage",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    def __str__(self):
        return self.title

    panels = [
        FieldPanel("title"),
        InlinePanel("bullets", label="Bullets"),
        FieldPanel("screenshot"),
        FieldPanel("video_url"),
        MediaChooserPanel("video"),
    ]


class FeaturePageFeatureAspect(Orderable, models.Model):
    page = ParentalKey("features.FeatureDescription", related_name="feature_aspects")
    feature_aspect = models.ForeignKey(
        "features.FeatureAspect", models.CASCADE, related_name="+"
    )

    panels = [FieldPanel("feature_aspect")]


@register_snippet
class FeatureDescription(ClusterableModel):
    title = models.CharField(max_length=255)
    introduction = models.CharField(max_length=255, blank=True)
    documentation_link = models.URLField(max_length=255, blank=True)
    panels = [
        FieldPanel("title"),
        FieldPanel("introduction"),
        FieldPanel("documentation_link"),
        InlinePanel("feature_aspects", label="Feature Aspects"),
    ]

    def __str__(self):
        return self.title


class FeatureIndexPageMenuOption(models.Model):
    page = ParentalKey(
        "features.FeatureIndexPage", related_name="secondary_menu_options"
    )
    link = models.ForeignKey("wagtailcore.Page", models.CASCADE, related_name="+")
    label = models.CharField(max_length=255)


class FeatureIndexPage(Page):
    template = "patterns/pages/feature_index_page/feature_index_page.html"

    subheading = models.TextField(verbose_name="Sub heading", blank=True)
    features = StreamField(
        [("features", FeatureIndexBlock())], blank=True, max_num=1, use_json_field=True
    )
    cta = StreamField(
        [("cta", StandaloneCTABlock())], blank=True, max_num=1, use_json_field=True
    )
    get_started = models.ForeignKey(
        "core.GetStartedSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subheading"),
        FieldPanel("features", classname="collapsible"),
        FieldPanel("cta", heading="Call to action"),
        FieldPanel("get_started"),
    ]
