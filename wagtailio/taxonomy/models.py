from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtailio.core.choices import SVGIcon


class Category(models.Model):
    title = models.CharField(max_length=128)
    short_title = models.CharField(max_length=64, blank=True)
    icon = models.CharField(choices=SVGIcon.choices, max_length=255, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("short_title"),
            ],
            "Title",
        ),
        FieldPanel("icon"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"
