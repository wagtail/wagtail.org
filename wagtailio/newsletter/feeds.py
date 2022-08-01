from datetime import datetime, time

from django.contrib.syndication.views import Feed
from django.http import Http404
from django.urls import reverse

from wagtailio.newsletter.models import NewsletterIndexPage, NewsletterPage


class NewsLetterIssuesFeed(Feed):
    title = "This week in Wagtail"
    description = "Our weekly, or thereabouts, newsletter of the goings-on in the Wagtail community."

    def link(self):
        root = NewsletterIndexPage.objects.live().public().first()
        if not root:
            raise Http404
        return root.full_url

    def items(self):
        return NewsletterPage.objects.live().public().order_by("-date")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro

    def item_link(self, item):
        return item.full_url

    def item_pubdate(self, item):
        return datetime.combine(item.date, time())
