from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter

from wagtailio.taxonomy.models import Category


class BlogPostFilterSet(FilterSet):
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.none(), label="Category"
    )
    author = CharFilter("authors__author__name", lookup_expr="iexact", label="Author")

    class Meta:
        # Referenced by string to avoid a circular import with wagtailio.blog.models.
        model = "blog.BlogPage"
        fields = []

    def __init__(self, *args, **kwargs):
        """Must be constructed with `queryset=` (e.g. BlogIndexPage.posts), which scopes the category choices."""
        super().__init__(*args, **kwargs)
        self.filters["category"].queryset = Category.objects.filter(
            pk__in=self.queryset.order_by().values("category")
        ).order_by("title")
