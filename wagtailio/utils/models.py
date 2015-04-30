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

class WagtailImage(AbstractImage):
    alternative_text = models.CharField(max_length=255, blank=True, help_text="The alternative text for the image, provided for the benefit of visually impaired users")

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=WagtailImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)

class WagtailRendition(AbstractRendition):
    image = models.ForeignKey('WagtailImage', related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )

# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=WagtailRendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)



class SocialMediaMixin(models.Model):
    social_text = models.CharField(max_length=255, blank=True, help_text="Description of this page as it should appear when shared on social networks, or in Google results")
    social_image = models.ForeignKey(
        'images.GlobalWitnessImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Image to appear alongside 'social text', particularly for sharing on social networks",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('social_text'),
            ImageChooserPanel('social_image')
        ], "Social/Meta descriptions")
    ]

    class Meta:
        abstract = True


class CrossPageMixin(models.Model):
    listing_image = models.ForeignKey('images.GlobalWitnessImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    listing_intro = models.TextField(blank=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('social_text'),
            ImageChooserPanel('social_image')
        ], "Cross-page behaviour")
    ]

    class Meta:
        abstract = True