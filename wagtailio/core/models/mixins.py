from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailio.core.blocks import CTABlock
from wagtailio.core.choices import SVGIcon


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
            [FieldPanel("social_text"), ImageChooserPanel("social_image")],
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
            [FieldPanel("listing_intro"), ImageChooserPanel("listing_image")],
            "Cross-page behaviour",
        )
    ]

    class Meta:
        abstract = True


class HeroMixin(models.Model):
    heading = models.TextField(verbose_name="Heading")
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    intro = RichTextField(
        verbose_name="Intro",
        blank=True,
        features=["bold", "italic", "link"],
    )
    icon = models.CharField(choices=SVGIcon.choices, max_length=255)
    cta = StreamField([("cta", CTABlock())], blank=True, max_num=1)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
                FieldPanel("intro"),
                FieldPanel("icon"),
                StreamFieldPanel("cta"),
            ],
            "Hero",
        )
    ]

    class Meta:
        abstract = True
