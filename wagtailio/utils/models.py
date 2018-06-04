from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page
from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel, InlinePanel
)

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

class LinkGroupLink(Orderable, models.Model):
    snippet = ParentalKey('LinkGroupSnippet', related_name='links')
    link_URL = models.URLField(help_text="Choose a URL to which to link")
    link_text = models.TextField(help_text="Text of the link")
    link_description = models.TextField(blank=True, help_text="Optional")
    link_icon = models.TextField(null=True, blank=True, help_text="Optional. The code of a Fontawesome icon to display beside this link e.g fa-twitter", max_length=50)

    panels = [
        FieldPanel('link_URL'),
        FieldPanel('link_text'),
        FieldPanel('link_description'),
        FieldPanel('link_icon')
    ]


class LinkGroupSnippet(ClusterableModel):
    name = models.CharField(max_length=255, help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.")
    panels = [
        FieldPanel('name'),
        InlinePanel('links', label='Links')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Link group"
        ordering = ['name']

register_snippet(LinkGroupSnippet)


class MenuSnippetLink(Orderable, models.Model):
    snippet = ParentalKey('MenuSnippet', related_name='links')
    link_page = models.ForeignKey('wagtailcore.Page', models.SET_NULL, null=True, blank=True, related_name='+', help_text="Choose a page to which to link")
    link_text = models.TextField(blank=True, help_text="Optional. Override title text for chosen link page")

    panels = [
        PageChooserPanel('link_page'),
        FieldPanel('link_text')
    ]


class MenuSnippet(ClusterableModel):
    menu_name = models.CharField(max_length=255, help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.")
    panels = [
        FieldPanel('menu_name'),
        InlinePanel('links', label='Links')
    ]

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = "Menu"
        ordering = ['menu_name']

register_snippet(MenuSnippet)


class SocialMediaMixin(models.Model):
    social_text = models.CharField("Meta description", max_length=255, blank=True, help_text="Description of this page as it should appear when shared on social networks, or in Google results")
    social_image = models.ForeignKey('images.WagtailIOImage', models.SET_NULL, verbose_name="Meta image", null=True, blank=True, related_name='+', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks",)

    panels = [
        MultiFieldPanel([
            FieldPanel('social_text'),
            ImageChooserPanel('social_image')
        ], "Social/Meta descriptions")
    ]

    class Meta:
        abstract = True


class CrossPageMixin(models.Model):
    listing_image = models.ForeignKey('images.WagtailIOImage', models.SET_NULL, null=True, blank=True, related_name='+', help_text="Image to display along with summary, when this page is linked from elsewhere in the site.")
    listing_intro = models.TextField(blank=True, help_text="Summary of this page to display when this is linked from elsewhere in the site.")

    panels = [
        MultiFieldPanel([
            FieldPanel('listing_intro'),
            ImageChooserPanel('listing_image')
        ], "Cross-page behaviour")
    ]

    class Meta:
        abstract = True
