from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtailio.event_banner.models import EventBannerSettings


register = template.Library()

# Mapping of EventBannerSettings.theme to template modifier classes.
THEME_CLASSES = {
    EventBannerSettings.THEME_SPACE_INDIGO: "event-banner--space-indigo",
    EventBannerSettings.THEME_CLASSIC_TEAL: "event-banner--classic-teal",
}


def get_banner_context(banner_settings):
    """Build the template context for the banner from the settings."""
    illustration_url = ""
    if banner_settings.illustration:
        try:
            # Wagtail images have no direct URL; use a cached rendition
            # instead. Sized at 2x the desktop slot (73px) for retina.
            illustration_url = banner_settings.illustration.get_rendition(
                "max-160x160"
            ).url
        except (ValueError, OSError):
            # The image record has no usable file (e.g. a broken upload).
            # Fall back to the text-only banner rather than rendering an
            # image with an empty or broken URL.
            illustration_url = ""

    return {
        "theme_class": THEME_CLASSES.get(
            banner_settings.theme,
            THEME_CLASSES[EventBannerSettings.THEME_SPACE_INDIGO],
        ),
        "illustration": banner_settings.illustration,
        "illustration_url": illustration_url,
        "intro_text": banner_settings.intro_text,
        "title": banner_settings.title,
        "date_text": banner_settings.date_text,
        "cta_url": banner_settings.get_cta_url()
        if banner_settings.cta_button_text
        else "",
        "cta_text": banner_settings.cta_button_text,
    }


@register.simple_tag(takes_context=True)
def event_banner(context):
    """Render the site-wide event banner.

    The banner is only rendered when it is enabled for the current site and
    the current page's URL is not excluded in the settings.
    """
    request = context.get("request")
    if request is None:
        return ""

    banner_settings = EventBannerSettings.for_request(request)
    if not banner_settings.enabled:
        return ""

    page = context.get("page")
    if banner_settings.is_url_excluded(page):
        return ""

    # The markup is produced entirely by our own event_banner.html template
    # (autoescaped during render), not from untrusted input.
    return mark_safe(  # noqa: S308
        render_to_string(
            "event_banner/event_banner.html",
            get_banner_context(banner_settings),
            request=request,
        )
    )
