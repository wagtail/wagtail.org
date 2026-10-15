import datetime

import factory
import wagtail_factories

from wagtailio.newsletter.models import NewsletterIndexPage, NewsletterPage


class NewsletterIndexPageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Newsletter {n}")
    body = "<p>All the issues of the newsletter</p>"

    class Meta:
        model = NewsletterIndexPage


class NewsletterPageFactory(wagtail_factories.PageFactory):
    title = factory.Sequence(lambda n: f"Issue #{n}")
    date = datetime.date(2026, 1, 1)
    intro = "<p>The intro to the issue</p>"
    body = "<p>The body of the issue</p>"

    class Meta:
        model = NewsletterPage
