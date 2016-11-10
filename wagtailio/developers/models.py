from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                MultiFieldPanel,
                                                PageChooserPanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page

from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class DevelopersPageOptions(Orderable, models.Model):
    page = ParentalKey('developers.DevelopersPage', related_name='options')
    icon = models.CharField(max_length=255, choices=(
        ('github', 'Github'),
        ('social', 'Social'),
        ('documentation', 'Documentation')
    ))
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    external_link = models.URLField("External link", blank=True)

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        else:
            return self.external_link

    panels = [
        FieldPanel('icon'),
        FieldPanel('title'),
        FieldPanel('summary'),
        MultiFieldPanel([
            PageChooserPanel('internal_link'),
            FieldPanel('external_link')
        ], "Link")
    ]


class DevelopersPage(Page, SocialMediaMixin, CrossPageMixin):
    introduction = models.CharField(max_length=255)
    body_heading = models.CharField(max_length=255)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('body_heading'),
        FieldPanel('body'),
        InlinePanel('options', label="Options")
    ]
