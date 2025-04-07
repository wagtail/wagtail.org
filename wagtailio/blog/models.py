from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models import Case, IntegerField, Value, When
from django.db.models.functions import Lower
from django.shortcuts import render
from django.utils.functional import cached_property

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailio.blog.blocks import BlogStoryBlock
from wagtailio.taxonomy.models import Category
from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


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

    @cached_property
    def posts(self):
        # Get list of blog pages that are descendants of this page, ordered by date
        return (
            BlogPage.objects.live()
            .descendant_of(self)
            .select_related("author", "author__image", "category")
            .annotate(category_title_lower=Lower("category__title"))
            .order_by("-date", "pk")
        )

    @cached_property
    def categories(self):
        return (
            Category.objects.filter(
                pk__in=models.Subquery(self.posts.values("category"))
            )
            .annotate(title_lower=Lower("title"))
            .annotate(checked=Value(0))
        )

    def serve(self, request):
        posts = self.posts
        categories = self.categories
        category_selected = False

        if request.GET and not request.GET.get("all"):
            filtered_categories = list(request.GET)

            # Prevent non-category values being filtered
            if all(
                category in categories.values_list("title_lower", flat=True)
                for category in filtered_categories
            ):
                # Filter and annotate checked categories
                categories = categories.annotate(
                    checked=Case(
                        When(title_lower__in=filtered_categories, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                )
                posts = self.posts.filter(category_title_lower__in=filtered_categories)
                category_selected = True

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
                "categories": categories.values_list("pk", "title", "checked")
                .distinct()
                .order_by("title"),
                "category_selected": category_selected,
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


class BlogPage(Page, SocialMediaMixin, CrossPageMixin):
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

    content_panels = Page.content_panels + [
        FieldPanel("author"),
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
