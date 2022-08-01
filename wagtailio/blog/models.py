from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_airtable.mixins import AirtableMixin
from wagtail_content_import.models import ContentImportMixin

from wagtailio.utils.blocks import StoryBlock
from wagtailio.utils.mappers import StreamFieldMapper
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    subpage_types = ["blog.BlogPage"]

    @property
    def posts(self):
        # Get list of blog pages that are descendants of this page, ordered by date
        return (
            BlogPage.objects.live()
            .descendant_of(self)
            .select_related("author", "author__image")
            .order_by("-date", "pk")
        )

    def serve(self, request):
        # Pagination
        paginator = Paginator(self.posts, 10)  # Show 10 blog posts per page

        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = None

        return render(
            request,
            self.template,
            {
                "page": self,
                "posts": posts,
            },
        )

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


class BlogPage(
    AirtableMixin, Page, ContentImportMixin, SocialMediaMixin, CrossPageMixin
):
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

    mapper_class = StreamFieldMapper  # used for content import

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
            # "slug" not included so Airtable cannot overwrite the Page slug as
            # that could cause a lot of trouble with URLs and SEO. But it's possible
            # to do this assuming there aren't two pages with the same slug.
        }
        return mappings

    def get_export_fields(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Live": self.live,
            "Slug": self.slug,
            "Author": getattr(self.author, "name", ""),
        }
