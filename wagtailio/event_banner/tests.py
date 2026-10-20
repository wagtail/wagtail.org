from unittest.mock import MagicMock

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from wagtail.models import Page

from wagtailio.event_banner.models import EventBannerSettings
from wagtailio.event_banner.templatetags.event_banner_tags import get_banner_context


class EventBannerSettingsValidationTests(SimpleTestCase):
    def get_valid_settings(self):
        return EventBannerSettings(
            enabled=True,
            title="Wagtail Space 2026",
            cta_button_text="Register",
            cta_button_link="https://example.com/",
        )

    def test_clean_with_valid_data(self):
        self.get_valid_settings().clean()

    def test_clean_requires_title_when_enabled(self):
        settings = self.get_valid_settings()
        settings.title = ""
        with self.assertRaises(ValidationError):
            settings.clean()

    def test_clean_ignores_missing_title_when_disabled(self):
        settings = self.get_valid_settings()
        settings.enabled = False
        settings.title = ""
        settings.cta_button_text = ""
        settings.cta_button_link = ""
        settings.clean()

    def test_clean_rejects_cta_without_page_or_link(self):
        settings = self.get_valid_settings()
        settings.cta_button_link = ""
        with self.assertRaises(ValidationError):
            settings.clean()

    def test_clean_rejects_cta_with_both_page_and_link(self):
        settings = self.get_valid_settings()
        settings.cta_button_page = Page(pk=1)
        with self.assertRaises(ValidationError):
            settings.clean()

    def test_clean_rejects_cta_link_without_text(self):
        settings = self.get_valid_settings()
        settings.cta_button_text = ""
        with self.assertRaises(ValidationError):
            settings.clean()

    def test_clean_rejects_relative_excluded_urls(self):
        settings = self.get_valid_settings()
        settings.excluded_urls = "wagtail-space/"
        with self.assertRaises(ValidationError):
            settings.clean()


class ExcludedUrlPrefixesTests(SimpleTestCase):
    def test_normalises_trailing_slashes_and_ignores_noise(self):
        settings = EventBannerSettings(
            excluded_urls="/wagtail-space\n/events/\n\n# comment\n"
        )
        self.assertEqual(
            settings.excluded_url_prefixes, ["/wagtail-space/", "/events/"]
        )

    def test_empty(self):
        self.assertEqual(EventBannerSettings().excluded_url_prefixes, [])


class IsUrlExcludedTests(SimpleTestCase):
    def get_settings(self, excluded_urls):
        return EventBannerSettings(excluded_urls=excluded_urls)

    def test_matches_section_and_subpages(self):
        settings = self.get_settings("/wagtail-space/")
        for url in ["/wagtail-space/", "/wagtail-space/schedule/"]:
            fake_page = type("FakePage", (), {"url": url})()
            self.assertTrue(settings.is_url_excluded(fake_page))

    def test_does_not_match_partial_segments(self):
        settings = self.get_settings("/wagtail-space/")
        fake_page = type("FakePage", (), {"url": "/wagtail-space-2026/"})()
        self.assertFalse(settings.is_url_excluded(fake_page))

    def test_does_not_match_other_pages(self):
        settings = self.get_settings("/wagtail-space/")
        fake_page = type("FakePage", (), {"url": "/blog/some-post/"})()
        self.assertFalse(settings.is_url_excluded(fake_page))

    def test_no_page(self):
        settings = self.get_settings("/wagtail-space/")
        self.assertFalse(settings.is_url_excluded(None))

    def test_no_exclusions(self):
        settings = self.get_settings("")
        fake_page = type("FakePage", (), {"url": "/wagtail-space/"})()
        self.assertFalse(settings.is_url_excluded(fake_page))


class GetBannerContextTests(SimpleTestCase):
    def test_theme_class_mapping(self):
        cases = [
            (EventBannerSettings.THEME_WAGTAIL_SPACE, "event-banner--wagtail-space"),
            (EventBannerSettings.THEME_WHATS_NEW, "event-banner--whats-new"),
        ]
        for theme, expected_class in cases:
            with self.subTest(theme=theme):
                banner = EventBannerSettings(theme=theme)
                self.assertEqual(
                    get_banner_context(banner)["theme_class"], expected_class
                )

    def test_unknown_theme_falls_back_to_wagtail_space(self):
        banner = EventBannerSettings(theme="nonsense")
        self.assertEqual(
            get_banner_context(banner)["theme_class"], "event-banner--wagtail-space"
        )

    def test_illustration_is_none_by_default(self):
        banner = EventBannerSettings(theme=EventBannerSettings.THEME_WAGTAIL_SPACE)
        self.assertIsNone(get_banner_context(banner)["illustration"])

    def test_illustration_is_passed_through(self):
        illustration = MagicMock()
        banner = MagicMock(spec=EventBannerSettings)
        banner.theme = EventBannerSettings.THEME_WHATS_NEW
        banner.illustration = illustration
        self.assertIs(get_banner_context(banner)["illustration"], illustration)

    def test_cta_url_uses_link_when_text_present(self):
        banner = EventBannerSettings(
            cta_button_text="Register", cta_button_link="https://example.com/"
        )
        self.assertEqual(get_banner_context(banner)["cta_url"], "https://example.com/")

    def test_cta_url_empty_without_text(self):
        banner = EventBannerSettings(cta_button_link="https://example.com/")
        self.assertEqual(get_banner_context(banner)["cta_url"], "")
