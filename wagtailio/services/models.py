from django.db import models
from wagtail.admin import edit_handlers
from wagtail.core import fields
from wagtail.core.models import Page

from wagtailio.services.blocks import SectionBlock

class ServicesPage(Page):
    intro = models.TextField(null=True, blank=True)
    body = fields.StreamField([
        ('section', SectionBlock())
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        edit_handlers.FieldPanel("intro"),
        edit_handlers.StreamFieldPanel("body"),
    ]