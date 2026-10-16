import datetime

from django.test import TestCase

from wagtail.models import Page, Site

from wagtailio.core.factories import HomePageFactory
from wagtailio.newsletter.factories import (
    NewsletterIndexPageFactory,
    NewsletterPageFactory,
)


class NewsletterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        home = HomePageFactory(parent=Page.get_first_root_node())
        Site.objects.update(root_page=home)
        cls.index = NewsletterIndexPageFactory(parent=home)
        cls.older = NewsletterPageFactory(
            parent=cls.index, title="Older issue", date=datetime.date(2025, 1, 1)
        )
        cls.newer = NewsletterPageFactory(
            parent=cls.index, title="Newer issue", date=datetime.date(2026, 1, 1)
        )
        NewsletterPageFactory(parent=cls.index, title="Draft issue", live=False)

    def test_index_renders(self):
        response = self.client.get(self.index.url)

        self.assertContains(response, "Newer issue")

    def test_issue_renders(self):
        response = self.client.get(self.newer.url)

        self.assertContains(response, "The body of the issue")

    def test_index_lists_live_issues_newest_first(self):
        response = self.client.get(self.index.url)

        self.assertEqual(
            [issue.title for issue in response.context["newsletters"]],
            ["Newer issue", "Older issue"],
        )

    def test_index_has_five_issues_per_page(self):
        for _ in range(5):
            NewsletterPageFactory(parent=self.index)

        first = self.client.get(self.index.url)
        second = self.client.get(self.index.url, {"page": 2})

        self.assertEqual(len(first.context["newsletters"]), 5)
        self.assertEqual(len(second.context["newsletters"]), 2)
