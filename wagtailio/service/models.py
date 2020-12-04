from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail_content_import.models import ContentImportMixin

from wagtailio.core import blocks
from wagtailio.utils.models import SocialMediaMixin, CrossPageMixin


class ServicePage(Page, ContentImportMixin, SocialMediaMixin, CrossPageMixin):
    template = "service/services_page.html"

    strapline = models.CharField(max_length=255, blank=True)
    intro = models.TextField(blank=True)
    cta = models.ForeignKey(
        'utils.CallToActionSnippet',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel("strapline", classname="full"),
        FieldPanel("intro", classname="full"),
        InlinePanel("services", label="Services"),
        SnippetChooserPanel('cta'),
    ]

    promote_panels = (
            Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )


class ServicePageService(Orderable, models.Model):
    page = ParentalKey("service.ServicePage", related_name="services")
    text = models.CharField(max_length=100)
    icon_name = models.CharField(
        max_length=255,
        choices=(
            ("tooling", "Tooling"),
            ("architecture", "Architecture"),
            ("review", "Review"),
            ("api", "API"),
            ("develop", "Develop"),
            ("migration", "Migration"),
            ("more", "More"),
        ),
    )
