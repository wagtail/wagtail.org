from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class SocialMediaMixin(models.Model):
    social_text = models.CharField(
        "Meta description",
        max_length=255,
        blank=True,
        help_text="Description of this page as it should appear when shared on social networks, or in Google results",
    )
    social_image = models.ForeignKey(
        "images.WagtailIOImage",
        models.SET_NULL,
        verbose_name="Meta image",
        null=True,
        blank=True,
        related_name="+",
        help_text="Image to appear alongside 'Meta description', particularly for sharing on social networks",
    )

    panels = [
        MultiFieldPanel(
            [FieldPanel("social_text"), FieldPanel("social_image")],
            "Social/Meta descriptions",
        )
    ]

    class Meta:
        abstract = True


class CrossPageMixin(models.Model):
    listing_image = models.ForeignKey(
        "images.WagtailIOImage",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Image to display along with summary, when this page is linked from elsewhere in the site.",
    )
    listing_intro = models.TextField(
        blank=True,
        help_text="Summary of this page to display when this is linked from elsewhere in the site.",
    )

    panels = [
        MultiFieldPanel(
            [FieldPanel("listing_intro"), FieldPanel("listing_image")],
            "Cross-page behaviour",
        )
    ]

    class Meta:
        abstract = True
