from django.test import TestCase

from wagtail.models import Page, Site

from wagtailio.core.factories import ContentPageFactory, HomePageFactory


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home = HomePageFactory(parent=Page.get_first_root_node())
        Site.objects.update(root_page=cls.home)
        cls.content_page = ContentPageFactory(parent=cls.home, title="About Wagtail")

    def test_home_page_renders(self):
        response = self.client.get(self.home.url)

        self.assertEqual(response.status_code, 200)

    def test_content_page_renders(self):
        response = self.client.get(self.content_page.url)

        self.assertContains(response, "About Wagtail")
