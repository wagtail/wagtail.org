from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel, InlinePanel
)

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


class SocialMediaMixin(models.Model):
    social_text = models.CharField("Meta description", max_length=255, blank=True, help_text="Description of this page as it should appear when shared on social networks, or in Google results")
    social_image = models.ForeignKey('images.WagtailIOImage', verbose_name="Meta image", null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks",)

    panels = [
        MultiFieldPanel([
            FieldPanel('social_text'),
            ImageChooserPanel('social_image')
        ], "Social/Meta descriptions")
    ]

    class Meta:
        abstract = True


class CrossPageMixin(models.Model):
    listing_image = models.ForeignKey('images.WagtailIOImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Image to display along with summary, when this page is linked from elsewhere in the site.")
    listing_intro = models.TextField(blank=True, help_text="Summary of this page to display when this is linked from elsewhere in the site.")

    panels = [
        MultiFieldPanel([
            FieldPanel('listing_intro'),
            ImageChooserPanel('listing_image')
        ], "Cross-page behaviour")
    ]

    class Meta:
        abstract = True