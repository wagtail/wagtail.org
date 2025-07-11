from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from wagtailio.core.blocks import CTABlock, ImageBlock, SpaceStoryBlock
from wagtailio.utils.models import SocialMediaMixin


@register_snippet
class SpaceSocialSnippet(models.Model):
    heading = models.CharField(max_length=255)
    subheading = RichTextField(max_length=255)
    social = StreamField(
        [
            (
                "social",
                blocks.StructBlock(
                    [
                        ("name", blocks.CharBlock()),
                        ("url", blocks.URLBlock()),
                        (
                            "logo",
                            ImageBlock(
                                help_text="Max image width of 100px for best results."
                            ),
                        ),
                    ],
                ),
            ),
        ]
    )

    class Meta:
        verbose_name = "Wagtail Space Social Menu"

    def __str__(self):
        return self.heading

    panels = [
        FieldPanel("heading"),
        FieldPanel("subheading"),
        FieldPanel("social"),
    ]


class WagtailSpaceIndexPage(
    SocialMediaMixin, Page
):  # TODO: Determine if CrossPageMixin is needed
    template = "patterns/pages/space_index_page/space_index_page.html"
    parent_page_types = ["core.HomePage"]
    subpage_types = ["wagtailspace.WagtailSpacePage"]

    # ----------------- Hero -----------------
    heading = models.TextField(verbose_name="Heading", blank=True)
    event_date_subhead = models.TextField(verbose_name="Event date", blank=True)
    tagline = models.TextField(verbose_name="Tagline", blank=True)
    cta = StreamField([("cta", CTABlock())], blank=True, max_num=2)
    body = StreamField(SpaceStoryBlock(), blank=True)
    space_social = models.ForeignKey(
        "wagtailspace.SpaceSocialSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("event_date_subhead"),
                FieldPanel("tagline"),
                FieldPanel("cta"),
            ],
            "Hero",
            classname="collapsible",
        ),
        FieldPanel("body"),
        FieldPanel("space_social"),
    ]


class WagtailSpacePage(SocialMediaMixin, Page):
    parent_page_types = ["wagtailspace.WagtailSpaceIndexPage"]
    template = "patterns/pages/space_page/space_page.html"
    heading = models.TextField(verbose_name="Heading", blank=True)
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    body = StreamField(SpaceStoryBlock(), blank=True)
    space_social = models.ForeignKey(
        "wagtailspace.SpaceSocialSnippet",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("space_social"),
    ]

    class Meta:
        verbose_name = "Wagtail Space Page"