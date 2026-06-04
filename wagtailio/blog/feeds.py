from datetime import datetime, time

from django.contrib.syndication.views import Feed

from wagtailio.blog.models import BlogPage


class BlogFeed(Feed):
    title = "The Wagtail CMS Blog"
    link = "/blog/"

    def items(self):
        return (
            BlogPage.objects.live()
            .public()
            .defer_streamfields()
            .prefetch_related("authors__author")
            .order_by("-date")[:20]
        )

    def item_title(self, item: BlogPage) -> str:
        return item.title

    def item_description(self, item: BlogPage) -> str:
        return item.introduction

    def item_link(self, item: BlogPage) -> str:
        return item.full_url

    def item_author_name(self, item: BlogPage) -> str | None:
        authors = [author_item.author.name for author_item in item.authors.all()]
        if not authors:
            return None

        return ", ".join(authors)

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())
