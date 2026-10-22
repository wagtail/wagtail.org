import operator

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe

from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting


@register_setting(icon="calendar-check")
class EventBannerSettings(BaseSiteSetting):
    class Meta:
        verbose_name = "Event banner"

    THEME_SPACE_INDIGO = "space_indigo"
    THEME_CLASSIC_TEAL = "classic_teal"

    THEME_CHOICES = [
        (THEME_SPACE_INDIGO, "Space Indigo (pink button)"),
        (THEME_CLASSIC_TEAL, "Classic Teal (green button)"),
    ]

    enabled = models.BooleanField(
        default=False,
        verbose_name="Enable event banner",
    )
    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default=THEME_SPACE_INDIGO,
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
            "square image at least 150 x 150 px with a "
            "transparent background. If no image is uploaded, the banner "
            "shows text only."
        ),
    )
    intro_text = models.CharField(
        blank=True,
        help_text="Small line shown before the illustration on larger screens, e.g. 'Join us for...'",
    )
    title = models.CharField(
        help_text="Main banner text, e.g. 'Wagtail Space 2026'",
    )
    date_text = models.CharField(
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

    excluded_paths = models.TextField(
        blank=True,
        verbose_name="Excluded Paths",
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
            [FieldPanel("excluded_paths")],
            "Excluded Paths",
            classname="collapsible",
        ),
    ]

    @property
    def excluded_url_prefixes(self):
        prefixes = []
        for raw_line in self.excluded_paths.splitlines():
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

        # Excluded paths validation
        for raw_line in self.excluded_paths.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("/"):
                raise ValidationError(
                    {
                        "excluded_paths": ValidationError(
                            f"'{line}' does not look like a URL path. "
                            "Each line must start with '/', e.g. '/wagtail-space/'."
                        ),
                    }
                )
