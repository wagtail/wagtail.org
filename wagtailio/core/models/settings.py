from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_setting(icon="list-ul")
class NavigationSettings(BaseSetting, ClusterableModel):
    footer_navigation = models.ForeignKey(
        "core.FooterMenuSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        SnippetChooserPanel("footer_navigation"),
    ]
