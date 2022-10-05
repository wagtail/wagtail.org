from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.models import Page
from wagtail.utils.urlpatterns import decorate_urlpatterns

from wagtailio.api import api_router
from wagtailio.blog.feeds import BlogFeed
from wagtailio.newsletter.feeds import NewsLetterIssuesFeed
from wagtailio.search.views import search
from wagtailio.sitewide_alert import urls as sitewide_alert_urls
from wagtailio.utils.cache import get_default_cache_control_decorator
from wagtailio.utils.views import favicon, robots, test_500_error

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("search/", search, name="search"),
    path("sitewide_alert/", include(sitewide_alert_urls, namespace="sitewide_alert")),
    path("api/v2/", api_router.urls),
] + decorate_urlpatterns([path("documents/", include(wagtaildocs_urls))], never_cache)

urlpatterns = [
    path("newsletter/feed/", NewsLetterIssuesFeed(), name="newsletter_feed"),
    path("blog/feed/", BlogFeed(), name="blog_feed"),
    path("sitemap.xml", sitemap),
    path("favicon.ico", favicon),
    path("robots.txt", robots),
]


Page.serve = get_default_cache_control_decorator()(Page.serve)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "PATTERN_LIBRARY_ENABLED", False) and apps.is_installed(
    "pattern_library"
):
    urlpatterns += [
        path("pattern-library/", include("pattern_library.urls")),
        path("test500", test_500_error),
    ]

# Set public URLs to use public cache.
urlpatterns = decorate_urlpatterns(urlpatterns, get_default_cache_control_decorator())


urlpatterns = private_urlpatterns + urlpatterns + [path("", include(wagtail_urls))]

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).

urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers(
        "Cookie", "X-Requested-With", "X-Forwarded-Proto", "Accept-Encoding"
    ),
)

# Error handlers
handler404 = "wagtailio.utils.views.error_404"
handler500 = "wagtailio.utils.views.error_500"
