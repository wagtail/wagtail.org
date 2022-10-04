from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Orderable, Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_airtable.mixins import AirtableMixin
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
        ImageChooserPanel("screenshot"),
        FieldPanel("video_url"),
        MediaChooserPanel("video"),
    ]


class FeaturePageFeatureAspect(Orderable, models.Model):
    page = ParentalKey("features.FeatureDescription", related_name="feature_aspects")
    feature_aspect = models.ForeignKey(
        "features.FeatureAspect", models.CASCADE, related_name="+"
    )

    panels = [SnippetChooserPanel("feature_aspect")]


@register_snippet
class FeatureDescription(AirtableMixin, ClusterableModel):
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

    @classmethod
    def map_import_fields(cls):
        """
        Maps Airtable columns to Django Model Fields.
        """
        mappings = {
            "Title": "title",
            "Introduction": "introduction",
            "Documentation": "documentation_link",
        }
        return mappings

    def get_export_fields(self):
        """
        Get field mappings for Airtable when saving a model object.
        """
        return {
            "ID": self.id,
            "Title": self.title,
            "Introduction": self.introduction,
            "Documentation": self.documentation_link,
        }


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
        StreamFieldPanel("features", classname="collapsible"),
        StreamFieldPanel("cta", heading="Call to action"),
        SnippetChooserPanel("get_started"),
    ]
