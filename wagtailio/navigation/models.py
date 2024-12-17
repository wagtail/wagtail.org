from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
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
    sections = StreamField(NavStreamField())

    panels = [
        FieldPanel("name"),
        FieldPanel("sections"),
    ]

    class Meta:
        verbose_name = "Footer menu"

    def __str__(self) -> str:
        return f"FooterMenu: {self.name}"

    def save(self, **kwargs):
        super().save(**kwargs)

        for nav in NavigationSettings.objects.filter(footer_navigation=self):
            nav.save(fragment_to_clear="footernav")


@register_snippet
class MainMenu(ClusterableModel):
    name = models.CharField(max_length=255)
    menu_sections = StreamField([("menu_section", MainMenuSectionBlock())])

    panels = [
        FieldPanel("name"),
        FieldPanel("menu_sections", classname="collapsible"),
    ]

    class Meta:
        verbose_name = "Main menu"

    def __str__(self) -> str:
        return f"Main menu: {self.name}"

    def save(self, **kwargs):
        super().save(**kwargs)

        for nav in NavigationSettings.objects.filter(main_navigation=self):
            nav.save(fragment_to_clear="primarynav")


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

    def save(self, **kwargs):
        fragment_to_clear = kwargs.pop("fragment_to_clear", None)
        super().save(**kwargs)

        if fragment_to_clear is not None:
            fragment_key_seeds = [fragment_to_clear]
        else:
            fragment_key_seeds = ["primarynav", "footernav"]
        keys = [
            # The fragment cache varies on:
            # the current site pk, whether used in preview, or in the pattern library
            make_template_fragment_key(key, vary_on=[self.site.pk, False, False])
            for key in fragment_key_seeds
        ]
        cache.delete_many(keys)
