from django.db import models
from django.shortcuts import redirect

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)


class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    subpage_types = ['blog.BlogPage']

    def serve(self, request):
        latest_blog = BlogPage.objects.live().order_by('-date').first()
        return redirect(latest_blog.url)

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + \
        CrossPageMixin.panels


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('job_title'),
        ImageChooserPanel('image'),
        FieldPanel('url')
    ]


class BlogPage(Page, SocialMediaMixin, CrossPageMixin):
    subpage_types = []
    canonical_url = models.URLField(blank=True)
    author = models.ForeignKey(
        'blog.Author',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    main_image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date = models.DateField()
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    @property
    def siblings(self):
        return self.__class__.objects.live(
        ).sibling_of(self).order_by('-date')

    content_panels = Page.content_panels + [
        SnippetChooserPanel('author'),
        ImageChooserPanel('main_image'),
        FieldPanel('date'),
        FieldPanel('introduction'),
        StreamFieldPanel('body')
    ]

    promote_panels = (
        Page.promote_panels +
        SocialMediaMixin.panels +
        CrossPageMixin.panels +
        [
            FieldPanel('canonical_url'),
        ]
    )
