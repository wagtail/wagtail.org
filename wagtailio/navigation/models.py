from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet

from wagtailio.navigation.blocks import MainMenuSectionBlock, NavStreamField


@register_snippet
class FooterMenu(models.Model):
    name = models.CharField(max_length=255)
    sections = StreamField(NavStreamField(), use_json_field=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("sections"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Footer menu"


@register_snippet
class MainMenu(ClusterableModel):

    name = models.CharField(max_length=255)
    menu_sections = StreamField(
        [("menu_section", MainMenuSectionBlock())], use_json_field=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("menu_sections", classname="collapsible"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Main menu"


@register_setting(icon="list-ul")
class NavigationSettings(BaseSiteSetting, ClusterableModel):
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
        FieldPanel("get_started_menu"),
        FieldPanel("main_navigation"),
        FieldPanel("footer_navigation"),
    ]