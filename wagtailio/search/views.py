from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.cache import add_never_cache_headers, patch_cache_control

from wagtail.models import Page
from wagtail.search.models import Query

from wagtailio.utils.cache import get_default_cache_control_kwargs


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)
    result_count = None
    promoted_page_pks = []

    # Search
    if search_query:
        query = Query.get(search_query)

        # Fetch relevant promoted page PK's
        promoted_page_pks = query.editors_picks.all().values_list("page__pk", flat=True)

        # Exclude them from search results so they are not shown twice.
        search_results = (
            Page.objects.live()
            .exclude(pk__in=promoted_page_pks)
            .specific()
            .search(search_query, operator="and")
        )

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # Include promoted results in search count
    if search_results:
        result_count = search_results.paginator.count + len(promoted_page_pks)
    else:
        result_count = len(promoted_page_pks)

    response = TemplateResponse(
        request,
        "patterns/pages/search_results/search_results.html",
        {
            "search_query": search_query,
            "search_results": search_results,
            "result_count": result_count,
        },
    )
    # Instruct FE cache to not cache when the search query is present.
    # It's so hits get added to the database and results include newly
    # added pages.
    if search_query:
        add_never_cache_headers(response)
    else:
        patch_cache_control(response, **get_default_cache_control_kwargs())
    return response
