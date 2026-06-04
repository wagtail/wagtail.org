from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

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
        "showcase.ShowcasePage",
        "features.FeatureIndexPage",
        "newsletter.NewsletterIndexPage",
        "standardpage.StandardPage",
        "packages.PackagesPage",
        "roadmap.RoadmapPage",
        "services.ServicesPage",
        "wagtailspace.WagtailSpaceIndexPage",
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

    # ----------------- Promo -----------------
    video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    autoplay_video = models.BooleanField(
        default=False,
        help_text="Automatically start the video when the video and page loads."
        "The video will start over again, every time it is finished",
    )
    code_snippet = models.TextField(
        blank=True,
        default="pip install wagtail",
    )
    call_to_action = StreamField(
        [("cta", CTABlock())],
        blank=True,
        max_num=2,
        help_text="Allows for a maximum of 2 CTA blocks",
        use_json_field=True,
    )

    body = StreamField(HomePageStoryBlock())

    hero_panels = [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
                FieldPanel("intro"),
                FieldPanel("icon"),
            ],
            "Hero",
            classname="collapsible",
        )
    ]
    promo_panels = [
        MultiFieldPanel(
            [
                MediaChooserPanel("video", media_type="video"),
                FieldPanel("autoplay_video"),
                FieldPanel("code_snippet"),
                FieldPanel("call_to_action"),
            ],
            "Promo",
            classname="collapsible",
        )
    ]

    content_panels = (
        Page.content_panels
        + hero_panels
        + promo_panels
        + [
            FieldPanel("body"),
        ]
    )

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.SearchField("sub_heading"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]


class ContentPage(Page, HeroMixin, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/content_page/content_page.html"

    parent_page_types = ["core.HomePage"]
    # subpage_types = []  # TODO

    body = StreamField(ContentStoryBlock())

    content_panels = Page.content_panels + HeroMixin.panels + [FieldPanel("body")]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.SearchField("sub_heading"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]
