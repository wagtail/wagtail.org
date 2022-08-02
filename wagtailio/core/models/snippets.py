from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet


class LinkGroupLink(Orderable, models.Model):
    snippet = ParentalKey("LinkGroupSnippet", related_name="links")
    link_URL = models.URLField(help_text="Choose a URL to which to link")
    link_text = models.TextField(help_text="Text of the link")
    link_description = models.TextField(blank=True, help_text="Optional")
    link_icon = models.TextField(
        null=True,
        blank=True,
        help_text="Optional. The code of a Fontawesome icon to display beside this link e.g fa-twitter",
        max_length=50,
    )

    panels = [
        FieldPanel("link_URL"),
        FieldPanel("link_text"),
        FieldPanel("link_description"),
        FieldPanel("link_icon"),
    ]


class LinkGroupSnippet(ClusterableModel):
    name = models.CharField(
        max_length=255,
        help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.",
    )
    panels = [FieldPanel("name"), InlinePanel("links", label="Links")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Link group"
        ordering = ["name"]


register_snippet(LinkGroupSnippet)


class MenuSnippetLink(Orderable, models.Model):
    snippet = ParentalKey("MenuSnippet", related_name="links")
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        help_text="Choose a page to which to link",
    )
    link_text = models.TextField(
        blank=True, help_text="Optional. Override title text for chosen link page"
    )

    panels = [PageChooserPanel("link_page"), FieldPanel("link_text")]


class MenuSnippet(ClusterableModel):
    menu_name = models.CharField(
        max_length=255,
        help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.",
    )
    panels = [FieldPanel("menu_name"), InlinePanel("links", label="Links")]

    def __str__(self):
        return self.menu_name

    class Meta:
        verbose_name = "Menu"
        ordering = ["menu_name"]


register_snippet(MenuSnippet)
