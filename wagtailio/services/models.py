from django.db import models
from wagtail.admin import edit_handlers
from wagtail.core.models import Page


class ServicesPage(Page):
    intro = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel("intro"),
    ]