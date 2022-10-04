from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.models import Orderable, Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from wagtail_airtable.mixins import AirtableMixin
from wagtail_content_import.models import ContentImportMixin

from wagtailio.blog.blocks import BlogStoryBlock
from wagtailio.taxonomy.models import Category
from wagtailio.utils.mappers import StreamFieldMapper
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


class FeaturedPost(Orderable):
    parent = ParentalKey("blog.BlogIndexPage", related_name="featured_posts")
    page = models.ForeignKey(
        "blog.BlogPage",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [PageChooserPanel("page")]


class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/blog/blog_index_page.html"
    subpage_types = ["blog.BlogPage"]

    @property
    def posts(self):
        # Get list of blog pages that are descendants of this page, ordered by date
        return (
            BlogPage.objects.live()
            .descendant_of(self)
            .select_related("author", "author__image", "category")
            .order_by("-date", "pk")
        )

    def serve(self, request):

        if request.GET.get("category"):
            posts = self.posts.filter(category=request.GET.get("category"))
        else:
            posts = self.posts

        # Pagination
        paginator = Paginator(posts, 10)  # Show 10 blog posts per page

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
                "featured_posts": [post.page for post in self.featured_posts.all()],
                "categories": Category.objects.filter(
                    pk__in=models.Subquery(self.posts.values("category"))
                )
                .values_list("pk", "title")
                .distinct()
                .order_by("title"),
            },
        )

    content_panels = Page.content_panels + [
        InlinePanel(
            "featured_posts",
            heading="Featured posts",
            label="Blog page",
            max_num=5,
        ),
    ]

    promote_panels = (
        Page.promote_panels + SocialMediaMixin.panels + CrossPageMixin.panels
    )


class BlogPageRelatedPage(Orderable):
    parent = ParentalKey("blog.BlogPage", related_name="related_posts")
    page = models.ForeignKey(
        "blog.BlogPage",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [PageChooserPanel("page")]


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
    template = "patterns/pages/blog/blog_page.html"
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
    category = models.ForeignKey(
        "taxonomy.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BlogStoryBlock())

    @property
    def siblings(self):
        return self.__class__.objects.live().sibling_of(self).order_by("-date")

    mapper_class = StreamFieldMapper  # used for content import

    content_panels = Page.content_panels + [
        SnippetChooserPanel("author"),
        ImageChooserPanel("main_image"),
        FieldPanel("date"),
        FieldPanel("category"),
        FieldPanel("introduction"),
        StreamFieldPanel("body"),
        InlinePanel(
            "related_posts",
            heading="Related pages",
            label="Related page",
            max_num=2,
        ),
    ]

    promote_panels = (
        Page.promote_panels
        + SocialMediaMixin.panels
        + CrossPageMixin.panels
        + [FieldPanel("canonical_url")]
    )

    @cached_property
    def related_pages(self):
        return self.related_posts.all()

    @cached_property
    def meta_text(self):
        if self.category:
            return self.category.title
        return None

    @cached_property
    def meta_icon(self):
        if self.category:
            return self.category.icon
        return None

    @property
    def publication_date(self):
        return self.date

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
