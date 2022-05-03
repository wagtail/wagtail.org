from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtailio.core.blocks import CodePromoBlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class DevelopersPageOptions(Orderable, models.Model):
    page = ParentalKey("developers.DevelopersPage", related_name="options")
    icon = models.CharField(
        max_length=255,
        choices=(
            ("github", "Github"),
            ("social", "Social"),
            ("documentation", "Documentation"),
        ),
    )
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    internal_link = models.ForeignKey(
        "wagtailcore.Page", models.CASCADE, null=True, blank=True, related_name="+"
    )
    external_link = models.URLField("External link", blank=True)

    @property
    def link(self):
        if self.internal_link:
            return self.internal_link.url
        else:
            return self.external_link

    panels = [
        FieldPanel("icon"),
        FieldPanel("title"),
        FieldPanel("summary"),
        MultiFieldPanel(
            [FieldPanel("internal_link"), FieldPanel("external_link")], "Link"
        ),
    ]


class DevelopersPage(Page, SocialMediaMixin, CrossPageMixin):
    body = StreamField(
        (
            (
                "code",
                CodePromoBlock(template="developers/blocks/code_with_link_block.html"),
            ),
        ), use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        InlinePanel("options", label="Options"),
    ]
