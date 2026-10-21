from unittest.mock import MagicMock

from django.template.loader import render_to_string
from django.test import SimpleTestCase

from wagtailio.event_banner.models import EventBannerSettings
from wagtailio.event_banner.templatetags.event_banner_tags import get_banner_context


class EventBannerRenderTests(SimpleTestCase):
    """Verify that the banner renders its markup.

    Runs DB-free: the settings object is mocked, exercising the full
    render path (context assembly + template) without needing the
    database.
    """

    def test_banner_renders(self):
        banner = MagicMock(spec=EventBannerSettings)
        banner.theme = EventBannerSettings.THEME_WAGTAIL_SPACE
        banner.illustration = MagicMock()
        banner.illustration.get_rendition.return_value.url = (
            "/media/images/test.max-160x160.png"
        )
        banner.intro_text = "Join us for..."
        banner.title = "Wagtail Space 2026"
        banner.date_text = "18-20 November"
        banner.cta_button_text = "Register"
        banner.get_cta_url.return_value = "https://example.com/register"

        html = render_to_string(
            "event_banner/event_banner.html", get_banner_context(banner)
        )

        # Banner container with the correct theme class
        self.assertIn("event-banner event-banner--wagtail-space", html)
        # All content elements present
        self.assertIn("Join us for...", html)
        self.assertIn("Wagtail Space 2026", html)
        self.assertIn("18-20 November", html)
        # CTA button with link
        self.assertIn('href="https://example.com/register"', html)
        self.assertIn("Register", html)
        # Illustration rendered via its rendition URL
        self.assertIn('src="/media/images/test.max-160x160.png"', html)
