from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.fields import StreamField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailio.navigation.blocks import MainMenuSectionBlock, NavStreamField


@register_snippet
class FooterMenu(models.Model):
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
class MainMenu(ClusterableModel):

    name = models.CharField(max_length=255)
    menu_sections = StreamField(
        [("menu_section", MainMenuSectionBlock())],
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("menu_sections", classname="collapsible"),
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
        "navigation.MainMenu",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    footer_navigation = models.ForeignKey(
        "navigation.FooterMenu",
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
