from django.test import TestCase
from django.urls import reverse

from wagtail.contrib.search_promotions.models import Query, SearchPromotion
from wagtail.models import Page, Site

from wagtailio.core.factories import ContentPageFactory, HomePageFactory


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        home = HomePageFactory(parent=Page.get_first_root_node())
        Site.objects.update(root_page=home)
        ContentPageFactory(parent=home, title="Zebrafish handbook")
        ContentPageFactory(parent=home, title="Zebrafish secrets", live=False)
        cls.unrelated = ContentPageFactory(parent=home, title="Quarterly accounts")

    def test_search_page_renders(self):
        response = self.client.get(reverse("search"))

        self.assertEqual(response.status_code, 200)

    def test_drafts_are_not_found(self):
        response = self.client.get(reverse("search"), {"query": "zebrafish"})

        self.assertContains(response, "Zebrafish handbook")
        self.assertNotContains(response, "Zebrafish secrets")

    def test_a_promoted_page_is_shown_even_if_it_does_not_match(self):
        SearchPromotion.objects.create(
            query=Query.get("zebrafish"), page=self.unrelated, sort_order=0
        )

        response = self.client.get(reverse("search"), {"query": "zebrafish"})

        self.assertContains(response, "Quarterly accounts")
