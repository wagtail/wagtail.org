from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailio.navigation.blocks import NavStreamField


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


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    footer_navigation = models.ForeignKey(
        "navigation.FooterMenuSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        SnippetChooserPanel("footer_navigation"),
    ]
