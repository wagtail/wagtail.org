from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, InlinePanel,
    PageChooserPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtailio.blog.models import BlogPage
from wagtailio.utils.models import (
    SocialMediaMixin,
    CrossPageMixin,
)


# Carousel items

class HomePageMainCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='main_carousel_items')
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=511)
    image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video = models.URLField()
    call_to_action_internal_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+'
    )
    call_to_action_external_link = models.URLField("Call to action URL", blank=True)
    call_to_action_caption = models.CharField(max_length=255, blank=True)

    @property
    def call_to_action_link(self):
        if self.call_to_action_internal_link:
            return self.call_to_action_internal_link.url
        else:
            return self.call_to_action_external_link

    panels = [
        FieldPanel('title'),
        FieldPanel('summary'),
        ImageChooserPanel('image'),
        FieldPanel('video'),
        MultiFieldPanel([
            PageChooserPanel('call_to_action_internal_link'),
            FieldPanel('call_to_action_external_link'),
            FieldPanel('call_to_action_caption')
        ], "Call To Action")
    ]


class HomePageSecondaryCarouselItem(Orderable, models.Model):
    page = ParentalKey('core.HomePage', related_name='secondary_carousel_items')
    title = models.CharField(max_length=255)
    desktop_image = models.ForeignKey(
        'images.WagtailIOImage',
        related_name='+'
    )
    mobile_image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    blockquote = models.TextField()
    author_name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'images.WagtailIOImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author_job = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    panels = [
        FieldPanel('title'),
        ImageChooserPanel('desktop_image'),
        ImageChooserPanel('mobile_image'),
        FieldPanel('blockquote'),
        FieldPanel('author_name'),
        ImageChooserPanel('author_image'),
        FieldPanel('author_job'),
        FieldPanel('website')
    ]


# Homepage

class HomePage(Page, SocialMediaMixin, CrossPageMixin):
    secondary_carousel_introduction = models.CharField(max_length=511)

    content_panels = Page.content_panels + [
        InlinePanel('main_carousel_items', label="Main carousel items"),
        FieldPanel('secondary_carousel_introduction'),
        InlinePanel('secondary_carousel_items', label="Secondary carousel items"),
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context.update({
            'blog_posts': BlogPage.objects.live().order_by('-date'),
        })

        return context
