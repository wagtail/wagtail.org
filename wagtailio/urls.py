from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from wagtail.contrib.sitemaps.views import sitemap
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from wagtail.core.models import Page
from wagtail.utils.urlpatterns import decorate_urlpatterns

from wagtail_ab_testing import urls as ab_testing_urls
from wagtail_content_import import urls as wagtail_content_import_urls
from wagtail_transfer import urls as wagtailtransfer_urls

from wagtailio.blog.feeds import BlogFeed
from wagtailio.newsletter.feeds import NewsLetterIssuesFeed
from wagtailio.utils.views import favicon, robots
from wagtailio.utils.cache import get_default_cache_control_decorator

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("", include(wagtail_content_import_urls)),
    path("wagtail-transfer/", include(wagtailtransfer_urls)),
] + decorate_urlpatterns([path("documents/", include(wagtaildocs_urls))], never_cache)

urlpatterns = [
    path('abtesting/', include(ab_testing_urls)),
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
