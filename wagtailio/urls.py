from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from wagtail.contrib.sitemaps.views import sitemap
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.search import urls as wagtailsearch_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from wagtailio.blog.feeds import BlogFeed
from wagtailio.newsletter import views
from wagtailio.utils.views import favicon


admin.autodiscover()


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('blog/feed/', BlogFeed(), name='blog_feed'),
    path('sitemap.xml', sitemap),
    path('favicon.ico', favicon),

    path('', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
