from django.core.exceptions import ValidationError
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtailio.core.blocks import (
    ContentStoryBlock,
    CTABlock,
    HomePageStoryBlock,
    StandaloneCTABlock,
)
from wagtailio.core.choices import SVGIcon
from wagtailio.core.models import HeroMixin
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class HomePage(SocialMediaMixin, CrossPageMixin, Page):
    template = "patterns/pages/home/home_page.html"
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "blog.BlogIndexPage",
        "core.ContentPage",
        "core.ShowcasePage",
        "features.FeatureIndexPage",
        "newsletter.NewsletterIndexPage",
        "standardpage.StandardPage",
        "packages.PackagesPage",
        "roadmap.RoadmapPage",
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

    body = StreamField(HomePageStoryBlock(), use_json_field=True)

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

    body = StreamField(ContentStoryBlock(), use_json_field=True)

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


class ShowcasePage(Page, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/showcase_page/showcase_page.html"
    htmx_template = "patterns/pages/showcase_page/showcase_page_fragment.html"

    parent_page_types = ["core.HomePage"]

    introduction = models.TextField(
        verbose_name="Introduction",
        blank=True,
    )
    cta = StreamField(
        [("cta", StandaloneCTABlock())],
        blank=True,
        max_num=1,
        help_text="Allows for a maximum of 1 CTA blocks",
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("cta"),
        InlinePanel("showcase_items", label="Showcase items"),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )

    search_fields = Page.search_fields + [
        index.SearchField("description"),
        index.SearchField("introduction"),
    ]

    def _is_htmx_request(self, request):
        return request.headers.get("HX-Request") == "true"

    def _filter_used_sectors(self):
        return ["All"] + list(
            self.showcase_items.values_list("sector__name", flat=True).distinct()
        )

    def _filtered_showcase_items(self, sector):
        if sector in self._filter_used_sectors() and sector != "All":
            return self.showcase_items.filter(sector__name=sector)
        else:
            return self.showcase_items.all()

    def get_template(self, request, *args, **kwargs):
        if self._is_htmx_request(request):
            return self.htmx_template
        else:
            return self.template

    def serve(self, request):
        response = super().serve(request)
        if self._is_htmx_request(request):
            # We only return the fragment, rather than the whole page.
            new_url = self.url + "?" + request.GET.urlencode()
            response.headers["HX-Push"] = new_url
        return response

    def get_context(self, request):
        context = super().get_context(request)

        context |= {
            "sectors": self._filter_used_sectors(),
            "showcase_items": self._filtered_showcase_items(request.GET.get("sector")),
            "current_sector": request.GET.get("sector") or "All",
        }

        return context


class ShowcaseItem(Orderable):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        "images.WagtailIOImage",
        models.SET_NULL,
        null=True,
        related_name="+",
    )
    alt_text = models.CharField(max_length=255, blank=True)
    logo = models.ForeignKey(
        "images.WagtailIOImage",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    external_link = models.URLField(blank=True)
    internal_link = models.ForeignKey(
        "wagtailcore.Page",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    link_text = models.CharField(max_length=255)

    sector = models.ForeignKey(
        "Sector",
        models.CASCADE,
        null=False,
        blank=False,
        related_name="+",
    )

    page = ParentalKey(
        ShowcasePage,
        related_name="showcase_items",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("sector"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("alt_text"),
        FieldPanel("logo"),
        FieldPanel("external_link"),
        FieldPanel("internal_link"),
        FieldPanel("link_text"),
    ]

    def clean(self):
        if not self.external_link and not self.internal_link:
            raise ValidationError(
                "You must specify either an external or internal link"
            )
        if self.external_link and self.internal_link:
            raise ValidationError(
                "You must specify either an external or internal link, not both"
            )

        if self.logo and not self.image:
            raise ValidationError("You must specify an image when using a logo")

    def __str__(self):
        return self.title

    @property
    def url(self):
        if self.external_link:
            return self.external_link
        return self.internal_link.url

    @property
    def link_svg(self):
        if self.external_link:
            return "open-link"
        return "arrow"
