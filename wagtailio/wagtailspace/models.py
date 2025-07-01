from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtailmedia.edit_handlers import MediaChooserPanel

from wagtailio.core.blocks import SpaceStoryBlock, CTABlock
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin

class WagtailSpaceIndexPage(SocialMediaMixin, Page): #TODO: Determine if CrossPageMixin is needed
    template = "patterns/pages/wagtailspace/space_page.html"
    parent_page_types = ["core.HomePage"]
    # subpage_types = ["wagtailspace.WagtailSpacePage"]

    # ----------------- Hero -----------------
    heading = models.TextField(verbose_name="Heading", blank=True)
    event_date_subhead = models.TextField(
        verbose_name="Event date",
        blank=True)
    tagline = models.TextField(
        verbose_name="Tagline",
        blank=True)
    cta = StreamField([("cta", CTABlock())], blank=True, max_num=1)

    body = StreamField(SpaceStoryBlock(), blank=True)
    contact_subhead = RichTextField(
        verbose_name="Contact Subhead",
        blank=True,
        features=["bold", "italic", "link"],
    ) #TODO: Turn the contact and social media piece into a Snippet
    content_panels = (Page.content_panels 
    + [ MultiFieldPanel(
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
        FieldPanel("contact_subhead"),
       ]
    )

class WagtailSpacePage:
    heading = models.TextField(verbose_name="Heading", blank=True)
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    body = StreamField(SpaceStoryBlock(), blank=True)

    content_panels = Page.content_panels + [FieldPanel("body")]
