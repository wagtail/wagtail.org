import logging
import operator

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
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

    cta_button_text = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="CTA Text",
    )

    # This allows both internal and external URLs
    cta_button_link = models.URLField(blank=True, verbose_name="CTA Link")

    cta_button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="CTA Page"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("sitewide_alert_enabled"),
                FieldPanel("sitewide_alert_text"),
                FieldPanel("cta_button_text"),
                PageChooserPanel("cta_button_page"),
                FieldPanel("cta_button_link"),  # For external URLs
            ],
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
        # CTA validation
        if self.cta_button_text and not operator.xor(
            bool(self.cta_button_page), bool(self.cta_button_link)
        ):
            raise ValidationError(
                {
                    "cta_button_link": ValidationError(
                        "Please provide either an internal page OR an external URL (but not both)."
                    ),
                }
            )

        if self.cta_button_text:
            if not self.cta_button_page and not self.cta_button_link:
                raise ValidationError(
                    {
                        "cta_button_page": ValidationError(
                            "Please provide either an internal page or external URL for the CTA button."
                        ),
                    }
                )
            if self.cta_button_page and self.cta_button_link:
                raise ValidationError(
                    {
                        "cta_button_link": ValidationError(
                            "Please provide either an internal page OR an external URL, not both."
                        ),
                    }
                )

        # Check if link is provided without button text
        if (self.cta_button_page or self.cta_button_link) and not self.cta_button_text:
            raise ValidationError(
                {
                    "cta_button_text": ValidationError(
                        "Please provide button text for the CTA."
                    ),
                }
            )

    def get_cta_url(self):
        """Return the page URL if set, otherwise the external URL"""
        if self.cta_button_page:
            return self.cta_button_page.url
        return self.cta_button_link

    def save(self, *args, **kwargs):
        alert_url = self.site.root_url + reverse("sitewide_alert:sitewide_alert")
        purge_url_from_cache(alert_url)
        logging.info(f"Frontend cache purged for sitewide alert url ({alert_url})")

        super().save(*args, **kwargs)
