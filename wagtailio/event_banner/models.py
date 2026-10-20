import operator

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting


# Vary list shared by the template fragment cache in the event_banner
# template tag. Keep in sync with wagtailio/event_banner/templatetags.
EVENT_BANNER_FRAGMENT_KEY = "event_banner"


def purge_event_banner_cache(site_pk):
    cache.delete(
        make_template_fragment_key(EVENT_BANNER_FRAGMENT_KEY, vary_on=[site_pk])
    )


@register_setting(icon="megaphone")
class EventBannerSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "Event banner"

    THEME_WAGTAIL_SPACE = "wagtail_space"
    THEME_WHATS_NEW = "whats_new"

    THEME_CHOICES = [
        (THEME_WAGTAIL_SPACE, "Wagtail Space (dusty pink button)"),
        (THEME_WHATS_NEW, "What's new (teal button)"),
    ]

    enabled = models.BooleanField(
        default=False,
        verbose_name="Enable event banner",
    )
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default=THEME_WAGTAIL_SPACE,
        help_text="Controls the background gradient and button colour.",
    )
    illustration = models.ForeignKey(
        "images.WagtailioImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Illustration",
        help_text=(
            "Optional illustration shown next to the banner text. Ideal: a "
            "square image at least 256 x 256 px (e.g. 512 x 512), with a "
            "transparent background. If no image is uploaded, the banner "
            "shows text only."
        ),
    )
    intro_text = models.CharField(
        max_length=120,
        blank=True,
        help_text="Small line shown before the illustration on larger screens, e.g. 'Join us for...'",
    )
    title = models.CharField(
        max_length=100,
        help_text="Main banner text, e.g. 'Wagtail Space 2026'",
    )
    date_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Date shown after the title, e.g. '18-20 November'. Leave blank to hide.",
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
        verbose_name="CTA Page",
    )

    excluded_urls = models.TextField(
        blank=True,
        verbose_name="Excluded URLs",
        help_text=mark_safe(
            "The banner is hidden on these pages and all their sub-pages. "
            "One URL path per line, starting with <code>/</code>. "
            "e.g. <code>/wagtail-space/</code>"
        ),
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("enabled"),
                FieldPanel("theme"),
                FieldPanel("illustration"),
                FieldPanel("intro_text"),
                FieldPanel("title"),
                FieldPanel("date_text"),
            ],
            "Banner",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta_button_text"),
                PageChooserPanel("cta_button_page"),
                FieldPanel("cta_button_link"),  # For external URLs
            ],
            "CTA",
        ),
        MultiFieldPanel(
            [FieldPanel("excluded_urls")],
            "Excluded URLs",
            classname="collapsible",
        ),
    ]

    @property
    def excluded_url_prefixes(self):
        prefixes = []
        for raw_line in self.excluded_urls.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.endswith("/"):
                line += "/"
            prefixes.append(line)
        return prefixes

    def is_url_excluded(self, page):
        """Return True if the banner should not be shown on this page.

        Matching is done by URL path prefix, so an entry of
        ``/wagtail-space/`` hides the banner on ``/wagtail-space/`` and
        every page below it.
        """
        if page is None:
            return False

        page_url = getattr(page, "url", None) or ""
        if not page_url:
            return False

        return any(page_url.startswith(prefix) for prefix in self.excluded_url_prefixes)

    def get_cta_url(self):
        """Return the page URL if set, otherwise the external URL."""
        if self.cta_button_page:
            return self.cta_button_page.url
        return self.cta_button_link

    def clean(self):
        super().clean()

        if self.enabled and not self.title:
            raise ValidationError(
                {
                    "title": ValidationError(
                        "Please provide a title for the event banner."
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

        # Excluded URLs validation
        for raw_line in self.excluded_urls.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("/"):
                raise ValidationError(
                    {
                        "excluded_urls": ValidationError(
                            f"'{line}' does not look like a URL path. "
                            "Each line must start with '/', e.g. '/wagtail-space/'."
                        ),
                    }
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        purge_event_banner_cache(self.site.pk)
