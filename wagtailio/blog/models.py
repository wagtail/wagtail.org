from django.db import models
from django.shortcuts import redirect

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail_content_import.models import ContentImportMixin

from wagtail_airtable.mixins import AirtableMixin

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.mappers import StreamFieldMapper
from wagtailio.utils.models import SocialMediaMixin, CrossPageMixin


class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    subpage_types = ["blog.BlogPage"]

    def serve(self, request):
        latest_blog = BlogPage.objects.live().order_by("-date").first()
        return redirect(latest_blog.url)

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        "images.WagtailIOImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
        FieldPanel("job_title"),
        ImageChooserPanel("image"),
        FieldPanel("url"),
    ]


class BlogPage(AirtableMixin, Page, ContentImportMixin, SocialMediaMixin, CrossPageMixin):
    subpage_types = []
    canonical_url = models.URLField(blank=True)
    author = models.ForeignKey(
        "blog.Author",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    main_image = models.ForeignKey(
        "images.WagtailIOImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    date = models.DateField()
    introduction = models.CharField(max_length=511)
    body = StreamField(StoryBlock())

    @property
    def siblings(self):
        return self.__class__.objects.live().sibling_of(self).order_by("-date")

    mapper_class = StreamFieldMapper

    content_panels = Page.content_panels + [
        SnippetChooserPanel("author"),
        ImageChooserPanel("main_image"),
        FieldPanel("date"),
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
    ]

    promote_panels = (
        Page.promote_panels
        + SocialMediaMixin.panels
        + CrossPageMixin.panels
        + [FieldPanel("canonical_url")]
    )

    @classmethod
    def map_import_fields(cls):
        """
        Maps Airtable columns to Django Model Fields.
        """
        mappings = {
            "Title": "title",
            "Live": "live",
            # "slug" not included so Airtable cannot overwrite the Page slug as that could cause a lot of trouble with URLs and SEO. But it's possible to do this assuming there aren't two pages with the same slug.
        }
        return mappings

    def get_export_fields(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Live": self.live,
            "Slug": self.slug,
            "Author": getattr(self.author, 'name', '')
        }

    def save(self, user=None, **kwargs):
        publishing = False
        if self.pk and self._skip_signals:
            # if updating an existing instance from airtable
            old_live_status = BlogPage.objects.get(pk=self.pk).live
            # work out whether the live status is being updated from airtable
            # if so, publish or unpublish the page to achieve the change instead
            # to ensure all other corresponding fields (eg `live_revision`) are updated
            # too
            if not self.live and old_live_status:
                self.live = True
                self.unpublish(user=user, commit=False)
            elif self.live and not old_live_status:
                publishing = True
                self.live = False

        super().save(user=user, **kwargs)

        if publishing:
            new_revision = self.save_revision(user=user)
            new_revision.publish(user=user)
