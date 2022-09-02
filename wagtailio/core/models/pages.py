from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtailio.core.blocks import ContentStoryBlock, CTABlock, HomePageStoryBlock
from wagtailio.core.choices import SVGIcon
from wagtailio.core.models import HeroMixin
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class HomePage(SocialMediaMixin, CrossPageMixin, Page):
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

    # ----------------- Hero -----------------
    heading = models.TextField(verbose_name="Heading", blank=True)
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    intro = RichTextField(
        verbose_name="Intro",
        blank=True,
        features=["bold", "italic", "link"],
    )
    icon = models.CharField(choices=SVGIcon.choices, max_length=255, blank=True)

    code_snippet = models.TextField(
        blank=True,
        default="pip install wagtail",
    )
    call_to_action = StreamField(
        [("cta", CTABlock())],
        blank=True,
        max_num=2,
        help_text="Allows for a maximum of 2 CTA blocks",
    )
    video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    loop_video = models.BooleanField(default=False)
    autoplay_video = models.BooleanField(default=False)

    body = StreamField(HomePageStoryBlock())

    hero_panels = [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
                FieldPanel("intro"),
                FieldPanel("icon"),
                FieldPanel("code_snippet"),
                StreamFieldPanel("call_to_action"),
                MediaChooserPanel("video", media_type="video"),
                FieldPanel("loop_video"),
                FieldPanel("autoplay_video"),
            ],
            "Hero",
            classname="collapsible",
        )
    ]

    content_panels = (
        Page.content_panels
        + hero_panels
        + [
            StreamFieldPanel("body"),
        ]
    )

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )


class ContentPage(Page, HeroMixin, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/content_page/content_page.html"

    parent_page_types = ["core.HomePage"]
    # subpage_types = []  # TODO

    body = StreamField(ContentStoryBlock())

    content_panels = Page.content_panels + HeroMixin.panels + [StreamFieldPanel("body")]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )
