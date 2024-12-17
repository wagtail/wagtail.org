from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtailio.core.blocks import CTABlock
from wagtailio.core.choices import SVGIcon


class HeroMixin(models.Model):
    heading = models.TextField(verbose_name="Heading", blank=True)
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    intro = RichTextField(
        verbose_name="Intro",
        blank=True,
        features=["bold", "italic", "link"],
    )
    icon = models.CharField(choices=SVGIcon.choices, max_length=255, blank=True)
    cta = StreamField([("cta", CTABlock())], blank=True, max_num=1)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
                FieldPanel("intro"),
                FieldPanel("icon"),
                FieldPanel("cta"),
            ],
            "Hero",
        )
    ]

    class Meta:
        abstract = True

    @property
    def has_hero(self):
        return any([self.heading, self.sub_heading, self.intro, self.icon, self.cta])
