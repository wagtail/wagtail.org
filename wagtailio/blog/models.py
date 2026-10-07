from django.core.paginator import InvalidPage, Paginator
from django.db import models
from django.db.models import F
from django.http import Http404
from django.utils.functional import cached_property
from django.utils.http import urlencode

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailio.blog.blocks import BlogStoryBlock
from wagtailio.core.models import SchemaOrgMixin
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin
from wagtailio.utils.schema_org import get_organisation_schema


class FeaturedPost(Orderable):
    parent = ParentalKey("blog.BlogIndexPage", related_name="featured_posts")
    page = models.ForeignKey(
        "blog.BlogPage",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("page")]


class BlogIndexPage(Page, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/blog/blog_index_page.html"
    subpage_types = ["blog.BlogPage"]
    # List blog pages newest first in page choosers
    chooser_ordering = (F("blogpage__date").desc(nulls_last=True), "-pk")

    @property
    def posts(self):
        # Get list of blog pages that are descendants of this page, ordered by date
        return (
            BlogPage.objects.live()
            .descendant_of(self)
            .select_related("category", "main_image")
            .prefetch_related("authors__author__image")
            .order_by("-date", "pk")
        )

    def get_context(self, request, *args, **kwargs):
        from wagtailio.blog.filters import BlogPostFilterSet

        context = super().get_context(request, *args, **kwargs)

        filterset = BlogPostFilterSet(request.GET, queryset=self.posts)
        if not filterset.is_valid():
            raise Http404

        paginator = Paginator(filterset.qs, 10)
        try:
            page = paginator.page(request.GET.get("page", 1))
        except InvalidPage:
            raise Http404 from None

        is_filtered = any(filterset.form.cleaned_data.values())
        context.update(
            filterset=filterset,
            paginator_page=page,
            pagination_sequence=paginator.get_elided_page_range(
                page.number, on_each_side=2, on_ends=1
            ),
            featured_posts=(
                []
                if is_filtered
                else [featured.page for featured in self.featured_posts.all()]
            ),
        )
        return context

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
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [FieldPanel("page")]


@register_snippet
class Author(index.Indexed, models.Model):
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
        FieldPanel("image"),
        FieldPanel("url"),
    ]

    search_fields = [
        index.SearchField("name"),
        index.AutocompleteField("name"),
    ]


class BlogPageAuthor(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="authors")
    author = models.ForeignKey(
        "blog.Author",
        on_delete=models.CASCADE,
        related_name="+",
    )

    panels = [
        FieldPanel("author"),
    ]

    api_fields = [
        APIField("author", writable=True),
    ]


class BlogPage(SchemaOrgMixin, Page, SocialMediaMixin, CrossPageMixin):
    template = "patterns/pages/blog/blog_page.html"
    subpage_types = []
    canonical_url = models.URLField(blank=True)
    main_image = models.ForeignKey(
        "images.WagtailIOImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    date = models.DateField(null=True)
    introduction = models.CharField(max_length=511)
    category = models.ForeignKey(
        "taxonomy.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(BlogStoryBlock())

    api_fields = [
        APIField("canonical_url", writable=True),
        APIField("main_image", writable=True),
        APIField("date", writable=True),
        APIField("introduction", writable=True),
        APIField("category", writable=True),
        APIField("body", writable=True),
        APIField("authors", writable=True),
    ]

    @property
    def siblings(self):
        return self.__class__.objects.live().sibling_of(self).order_by("-date")

    content_panels = Page.content_panels + [
        InlinePanel(
            "authors",
            heading="Authors",
            label="Author",
            max_num=3,
        ),
        FieldPanel("main_image"),
        FieldPanel("date"),
        FieldPanel("category"),
        FieldPanel("introduction"),
        FieldPanel("body"),
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

    search_fields = Page.search_fields + [
        index.SearchField("introduction"),
        index.SearchField("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        index_url = self.get_parent().get_url(request)
        context["blog_index_url"] = index_url
        if self.category:
            query = urlencode({"category": self.category.pk})
            context["category_url"] = f"{index_url}?{query}"
        return context

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

    def page_ld_entity(self, request=None) -> dict:
        url = self.get_full_url(request)

        authors = []
        for blog_author in self.authors.all().select_related("author"):
            author = blog_author.author
            person = {
                "@type": "Person",
                "name": author.name,
                "jobTitle": author.job_title,
                "url": author.url,
            }
            authors.append({key: value for key, value in person.items() if value})

        image = self.social_image or self.main_image

        publisher = get_organisation_schema()
        if publisher:
            publisher = {k: v for k, v in publisher.items() if k != "@context"}

        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "@id": f"{url}#blogposting",
            "mainEntityOfPage": url,
            "headline": self.seo_title or self.title,
            "description": self.social_text
            or self.search_description
            or self.introduction,
            "datePublished": self.date.isoformat() if self.date else None,
            "dateModified": (
                self.last_published_at.isoformat() if self.last_published_at else None
            ),
            "articleSection": self.category.title if self.category else None,
            "author": authors,
            "image": (image.get_rendition("min-1200x630").full_url if image else None),
            "publisher": publisher,
        }
        return {key: value for key, value in schema.items() if value}
