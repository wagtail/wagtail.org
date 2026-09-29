from django.core.cache import cache
from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon="globe")
class OrganisationSchemaSettings(BaseSiteSetting):
    """schema.org Organization data for the home page"""

    class Meta:
        verbose_name = "organisation schema"

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(
        blank=True, help_text="One or two sentences on what the organisation does"
    )
    logo = models.ForeignKey(
        "images.WagtailIOImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    same_as = models.TextField(
        "Social profiles",
        blank=True,
        help_text="Full URLs of official profiles (GitHub, LinkedIn, etc.), one per line",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("description"),
                FieldPanel("logo"),
                FieldPanel("same_as"),
            ],
            heading="Organisation",
        ),
    ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete("organisation_schema")

    def to_schema_dict(self):
        organisation = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "@id": f"{self.site.root_url}/#organization",
            "name": self.name,
            "description": self.description,
            "url": self.site.root_url,
            "logo": (
                self.logo.get_rendition("max-600x600").full_url if self.logo else None
            ),
            "sameAs": [url.strip() for url in self.same_as.splitlines() if url.strip()],
        }
        return {key: value for key, value in organisation.items() if value}
