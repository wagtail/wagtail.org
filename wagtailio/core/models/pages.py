from django.core.exceptions import ValidationError
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailio.core.blocks import (
    ContentStoryBlock,
    CTABlock,
    HomePageStoryBlock,
    LoopingVideoBlock,
)
from wagtailio.core.models import HeroMixin
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class HomePage(HeroMixin, SocialMediaMixin, CrossPageMixin, Page):
    template = "patterns/pages/home/home_page.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "blog.BlogIndexPage",
        "core.ContentPage",
        "developers.DevelopersPage",
        "features.FeatureIndexPage",
        "newsletter.NewsletterIndexPage",
        "standardpage.StandardPage",
        "packages.PackagesPage",
        "services.ServicesPage",
    ]

    code_snippet = models.CharField(
        max_length=100,
        default="pip install wagtail",
    )
    call_to_action = StreamField(
        [("cta", CTABlock())],
        blank=True,
        max_num=2,
        help_text="Use this instead of the Hero CTA. Allows for a maximum of 2 CTA blocks",
    )

    video = StreamField(
        [
            (
                "looping_video_block",
                LoopingVideoBlock(),
            ),
        ],
        blank=True,
        max_num=1,
    )

    body = StreamField(HomePageStoryBlock())

    content_panels = (
        Page.content_panels
        + HeroMixin.panels
        + [
            FieldPanel("code_snippet"),
            StreamFieldPanel("call_to_action"),
            StreamFieldPanel("video"),
            StreamFieldPanel("body"),
        ]
    )

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    def clean(self):
        super().clean()
        if self.cta:
            raise ValidationError(
                "The Hero CTA field must be left blank. Use the Call to Action field instead."
            )

    def save(self, *args, **kwargs):
        if self.cta:
            self.full_clean()
        super().save(*args, *kwargs)


class ContentPage(Page, HeroMixin, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/content_page/content_page.html"

    parent_page_types = ["core.HomePage"]
    # subpage_types = []  # TODO

    body = StreamField(ContentStoryBlock())

    content_panels = Page.content_panels + HeroMixin.panels + [StreamFieldPanel("body")]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )
