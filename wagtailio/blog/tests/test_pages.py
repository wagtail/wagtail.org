import datetime

from django.test import TestCase

from wagtail.models import Page, Site

from wagtailio.blog.factories import BlogIndexPageFactory, BlogPageFactory
from wagtailio.core.factories import HomePageFactory
from wagtailio.taxonomy.factories import CategoryFactory


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        home = HomePageFactory(parent=Page.get_first_root_node())
        Site.objects.update(root_page=home)
        cls.index = BlogIndexPageFactory(parent=home)
        cls.news = CategoryFactory(title="News")
        cls.older = BlogPageFactory(
            parent=cls.index, title="Older post", date=datetime.date(2025, 1, 1)
        )
        cls.newer = BlogPageFactory(
            parent=cls.index,
            title="Newer post",
            date=datetime.date(2026, 1, 1),
            category=cls.news,
        )
        BlogPageFactory(parent=cls.index, title="Draft post", live=False)

    def test_index_renders(self):
        response = self.client.get(self.index.url)

        self.assertContains(response, "Newer post")

    def test_post_renders(self):
        response = self.client.get(self.newer.url)

        self.assertContains(response, "Newer post")

    def test_index_lists_live_posts_newest_first(self):
        self.assertEqual(list(self.index.posts), [self.newer, self.older])

    def test_index_filters_by_category(self):
        response = self.client.get(self.index.url, {"category": self.news.pk})

        self.assertEqual(
            [post.title for post in response.context["paginator_page"]], ["Newer post"]
        )

    def test_index_has_ten_posts_per_page(self):
        for _ in range(9):
            BlogPageFactory(parent=self.index)

        first = self.client.get(self.index.url)
        second = self.client.get(self.index.url, {"page": 2})

        self.assertEqual(len(first.context["paginator_page"]), 10)
        self.assertEqual(len(second.context["paginator_page"]), 1)

    def test_next_and_previous_posts(self):
        self.assertEqual(self.older.next_post, self.newer)
        self.assertEqual(self.newer.previous_post, self.older)
