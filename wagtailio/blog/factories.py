import datetime

import factory
import wagtail_factories

from wagtailio.blog.models import BlogIndexPage, BlogPage


class BlogIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Blog {n}")

    class Meta:
        model = BlogIndexPage


class BlogPageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Blog post {n}")
    date = datetime.date(2026, 1, 1)
    introduction = "A short introduction to the post"

    class Meta:
        model = BlogPage
