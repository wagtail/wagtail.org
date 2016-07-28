from django.db import models
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


@register_snippet
class Organisation(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Name of the parent organisation using Wagtail (e.g. NASA)",
    )
    logo = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',

    )
    description = models.TextField(
        blank=True,
        help_text="This currently isn't being shown on the site, but may be "
                  "in the future",
    )
    URL = models.URLField(
        blank=True,
        help_text="This currently isn't being show on the site, but may be in "
                  "the future"
    )

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('description'),
        FieldPanel('URL'),
    ]
