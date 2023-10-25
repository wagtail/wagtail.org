import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.frontend_cache.utils import purge_url_from_cache
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import RichTextField


@register_setting
class SiteWideAlertSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "Sitewide alert"

    sitewide_alert_enabled = models.BooleanField(
        default=False, verbose_name="Enable sitewide alert"
    )
    sitewide_alert_text = RichTextField(
        blank=True,
        features=["h2", "h3", "bold", "italic", "link"],
        verbose_name="Alert text",
    )

    background_colour = models.CharField(
        max_length=6,
        blank=True,
        help_text=mark_safe("Background RGB value. e.g. <code>fd5765</code>"),
    )
    text_colour = models.CharField(
        max_length=6,
        blank=True,
        help_text=mark_safe("Text colour RGB value. e.g. <code>ffffff</code>"),
    )

    panels = [
        MultiFieldPanel(
            [FieldPanel("sitewide_alert_enabled"), FieldPanel("sitewide_alert_text")],
            "Sitewide alert",
        ),
        MultiFieldPanel(
            [FieldPanel("background_colour"), FieldPanel("text_colour")],
            "Style",
            classname="collapsible",
        ),
    ]

    def clean(self):
        if self.sitewide_alert_enabled and not self.sitewide_alert_text:
            raise ValidationError(
                {
                    "sitewide_alert_text": ValidationError(
                        "To enable the sitewide alert, please specify the alert text."
                    ),
                }
            )

    def save(self, *args, **kwargs):
        alert_url = self.site.root_url + reverse("sitewide_alert:sitewide_alert")
        purge_url_from_cache(alert_url)
        logging.info(f"Frontend cache purged for sitewide alert url ({alert_url})")

        super().save(*args, **kwargs)
