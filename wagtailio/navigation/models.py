from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailio.navigation.blocks import NavItemBlock, NavItemCTA, NavStreamField
from wagtailio.navigation.forms import MainMenuSnippetForm


@register_snippet
class FooterMenuSnippet(models.Model):
    name = models.CharField(max_length=255)
    sections = StreamField(
        NavStreamField(),
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("sections"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Footer menu"


@register_snippet
class MainMenuItemSnippet(models.Model):
    name = models.CharField(max_length=255)
    nav_items = StreamField(
        [("nav_item", NavItemBlock())],
    )
    call_to_action = StreamField(
        [("cta", NavItemCTA())],
        blank=True,
        max_num=1,
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("nav_items", classname="collapsible"),
        StreamFieldPanel("call_to_action", classname="collapsible"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Main menu item"


class MainMenuItem(Orderable):
    parent = ParentalKey("navigation.MainMenuSnippet", related_name="menu_items")
    menu_item = models.ForeignKey(
        "navigation.MainMenuItemSnippet",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("menu_item"),
    ]


@register_snippet
class MainMenuSnippet(ClusterableModel):
    base_form_class = MainMenuSnippetForm

    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [InlinePanel("menu_items", label="Menu item", min_num=1, max_num=10)],
            heading="Menu items",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Main menu"


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    get_started_menu = models.ForeignKey(
        "core.GetStartedSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    main_navigation = models.ForeignKey(
        "navigation.MainMenuSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    footer_navigation = models.ForeignKey(
        "navigation.FooterMenuSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        SnippetChooserPanel("get_started_menu"),
        SnippetChooserPanel("main_navigation"),
        SnippetChooserPanel("footer_navigation"),
    ]
