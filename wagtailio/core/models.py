from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtailio.blog.models import BlogPage
from wagtailio.core.blocks import HomePageBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    body = StreamField(HomePageBlock(), use_json_field=True)
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "blog.BlogIndexPage",
        "developers.DevelopersPage",
        "features.FeatureIndexPage",
        "newsletter.NewsletterIndexPage",
        "standardpage.StandardPage",
        "packages.PackagesPage",
        "services.ServicesPage",
    ]
    content_panels = Page.content_panels + [FieldPanel("body")]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context.update({"blog_posts": BlogPage.objects.live().order_by("-date")})

        return context
