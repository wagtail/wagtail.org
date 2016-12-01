from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.wagtailcore.fields import StreamField

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel

from wagtailio.blog.models import BlogPage
from wagtailio.core.blocks import HomePageBlock
from wagtailio.utils.models import SocialMediaMixin, CrossPageMixin


class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    body = StreamField(HomePageBlock())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context.update({
            'blog_posts': BlogPage.objects.live().order_by('-date'),
        })

        return context
