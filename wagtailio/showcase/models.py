from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from wagtailio.core.blocks import StandaloneCTABlock
from wagtailio.showcase.snippets import Sector
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class ShowcasePage(SocialMediaMixin, CrossPageMixin, Page):
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

    listing_meta_description = models.CharField(
        max_length=255, blank=True, help_text="The description beneath the listing"
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
        index.SearchField("introduction"),
    ]

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
        if request.htmx:
            return self.htmx_template
        else:
            return self.template

    def get_context(self, request):
        context = super().get_context(request)
        sectors = {}

        for sector in self._filter_used_sectors():
            if sector == request.GET.get("sector"):
                sectors[sector] = "selected"
            else:
                sectors[sector] = ""

        # Pagination
        paginator = Paginator(
            self._filtered_showcase_items(request.GET.get("sector")), 6
        )  # Show 6

        page = request.GET.get("page")
        try:
            showcase_items = paginator.page(page)
        except PageNotAnInteger:
            showcase_items = paginator.page(1)
        except EmptyPage:
            showcase_items = None

        context |= {
            "sectors": sectors,
            "showcase_items": showcase_items,
            "current_sector": request.GET.get("sector") or "All",
        }

        return context


class ShowcaseItem(Orderable):
    page = ParentalKey(
        ShowcasePage,
        related_name="showcase_items",
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
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
        Sector,
        models.CASCADE,
        null=False,
        blank=False,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("sector"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("alt_text"),
        FieldPanel("logo"),
        MultiFieldPanel(
            [
                FieldPanel("external_link"),
                FieldPanel("internal_link"),
                FieldPanel("link_text"),
            ],
            heading="Link",
            classname="collapsible",
            icon="link",
        ),
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
