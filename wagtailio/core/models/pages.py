from django.db import models
from django.utils.functional import cached_property

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtailio.core.blocks import ContentStoryBlock, CTABlock, HomePageStoryBlock
from wagtailio.core.choices import SVGIcon
from wagtailio.core.models import HeroMixin, SchemaOrgMixin
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin
from wagtailio.utils.navigation_trees import build_page_tree, get_headings
from wagtailio.utils.schema_org import get_organisation_schema


class HomePage(SchemaOrgMixin, SocialMediaMixin, CrossPageMixin, Page):
    template = "patterns/pages/home/home_page.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "blog.BlogIndexPage",
        "core.ContentPage",
        "showcase.ShowcasePage",
        "features.FeatureIndexPage",
        "newsletter.NewsletterIndexPage",
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

    def page_ld_entity(self, request=None) -> dict:
        return get_organisation_schema() or {}


class ContentPage(Page, HeroMixin, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/content_page/content_page.html"

    parent_page_types = ["core.HomePage", "core.ContentPage"]
    subpage_types = ["core.ContentPage"]

    body = StreamField(ContentStoryBlock())
    show_in_page_navigation = models.BooleanField(
        "Show in-page navigation",
        default=False,
        help_text="Lists the headings in the rich text of this page. "
        "Replaces the section navigation if this page has one.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            HeroMixin.panels[0].children + [FieldPanel("show_in_page_navigation")],
            "Hero",
        ),
        FieldPanel("body"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    search_fields = Page.search_fields + [
        index.SearchField("heading"),
        index.SearchField("sub_heading"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    @cached_property
    def in_page_navigation(self):
        if not self.show_in_page_navigation:
            return []

        return get_headings(
            str(block.value["rich_text"].source)
            for block in self.body
            if block.block_type == "rich_text"
        )

    @cached_property
    def section_navigation(self):
        if not self.numchild:
            return []

        pages = self.get_descendants().live().public().in_menu()
        return build_page_tree(pages, self)
