from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtailschemaorg.models import PageLDMixin

from wagtailio.core.blocks import CTABlock
from wagtailio.core.choices import SVGIcon
from wagtailio.utils.schema_org import breadcrumbs_schema


class SchemaOrgMixin(PageLDMixin):
    def page_ld_entity(self, request=None) -> dict:
        return {}

    def ld_entity(self, request) -> dict:
        entity = {
            **super().ld_entity(request),
            "@context": "https://schema.org",
            "@type": "WebPage",
        }
        if breadcrumb := breadcrumbs_schema(self, request):
            entity["breadcrumb"] = breadcrumb
        return {key: value for key, value in entity.items() if value}

    def ld_entity_list(self, request):
        entities = [self.ld_entity(request), self.page_ld_entity(request)]
        return [entity for entity in entities if entity]


class HeroMixin(models.Model):
    heading = models.TextField(verbose_name="Heading", blank=True)
    sub_heading = models.TextField(verbose_name="Sub heading", blank=True)
    intro = RichTextField(
        verbose_name="Intro",
        blank=True,
        features=["bold", "italic", "link"],
    )
    icon = models.CharField(choices=SVGIcon.choices, max_length=255, blank=True)
    cta = StreamField([("cta", CTABlock())], blank=True, max_num=1)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
                FieldPanel("intro"),
                FieldPanel("icon"),
                FieldPanel("cta"),
            ],
            "Hero",
        )
    ]

    class Meta:
        abstract = True

    @property
    def has_hero(self):
        return any([self.heading, self.sub_heading, self.intro, self.icon, self.cta])
