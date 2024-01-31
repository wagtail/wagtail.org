from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name
