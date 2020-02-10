from datetime import datetime, time

from django.contrib.syndication.views import Feed

from wagtailio.blog.models import BlogPage


class BlogFeed(Feed):
    title = "The Wagtail CMS Blog"
    link = "/blog/"

    def items(self):
        return BlogPage.objects.live().public().order_by("-date")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction

    def item_link(self, item):
        return item.full_url

    def item_author_name(self, item):
        if not item.author:
            return None

        return item.author.name

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())
