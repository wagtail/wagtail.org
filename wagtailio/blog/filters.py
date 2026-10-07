from django_filters import CharFilter, FilterSet, ModelMultipleChoiceFilter

from wagtailio.blog.models import BlogPage
from wagtailio.taxonomy.models import Category


class BlogPostFilterSet(FilterSet):
    category = ModelMultipleChoiceFilter(
        queryset=Category.objects.none(), label="Category"
    )
    author = CharFilter("authors__author__name", lookup_expr="iexact", label="Author")

    class Meta:
        model = BlogPage
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["category"].queryset = Category.objects.filter(
            pk__in=self.queryset.order_by().values("category")
        ).order_by("title")
