from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet

from wagtailio.areweheadlessyet.blocks import HomePageBlock, TopicPageBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


@register_snippet
class WagtailHeadlessIssue(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)

    panels = [FieldPanel("title")]

    def __str__(self):
        return self.title

    @property
    def url(self):
        return f"https://github.com/wagtail/wagtail/issues/{self.number}/"


class AreWeHeadlessYetHomePage(Page, SocialMediaMixin, CrossPageMixin):
    THUMBS_UP = "thumbs up"
    THUMBS_DOWN = "thumbs down"
    ICON_CHOICES = [
        (THUMBS_UP, THUMBS_UP),
        (THUMBS_DOWN, THUMBS_DOWN),
    ]
    strapline_icon = models.CharField(
        max_length=15,
        choices=ICON_CHOICES,
        default=THUMBS_UP,
    )
    strapline_text = RichTextField(features=["bold", "italic"])
    body = StreamField(HomePageBlock())

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("strapline_icon"),
                FieldPanel("strapline_text"),
            ],
            "strapline",
        ),
        StreamFieldPanel("body"),
    ]

    api_fields = [
        APIField("strapline_icon"),
        APIField("strapline_text"),
        APIField("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    # Set this so that this page type can only be created under the root page.
    parent_page_types = ["wagtailcore.Page"]

    subpage_types = ["areweheadlessyet.AreWeHeadlessYetTopicPage"]

    # Ensure that only one page of this type can be created.
    max_count = 1


class AreWeHeadlessYetTopicPage(Page, SocialMediaMixin, CrossPageMixin):
    GREEN = "green"
    AMBER = "amber"
    RED = "red"
    COLOR_CHOICES = [
        (GREEN, GREEN),
        (AMBER, AMBER),
        (RED, RED),
    ]
    status_color = models.CharField(max_length=5, choices=COLOR_CHOICES)
    introduction = models.TextField(blank=True)
    body = StreamField(TopicPageBlock())

    content_panels = Page.content_panels + [
        FieldPanel("status_color"),
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

    api_fields = [
        APIField("status_color"),
        APIField("introduction"),
        APIField("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    parent_page_types = ["areweheadlessyet.AreWeHeadlessYetHomePage"]
    subpage_types = []
