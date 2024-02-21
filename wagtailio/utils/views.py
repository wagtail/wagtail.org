from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views import defaults


def favicon(request):
    try:
        favicon_path = settings.FAVICON_PATH
    except AttributeError:
        raise Http404
    return redirect(static(favicon_path), permanent=True)


def robots(request):
    content = "\n".join(["User-Agent: *", "Disallow: /search/", "Allow: /"])
    return HttpResponse(content, content_type="text/plain")


def error_404(request, exception=None):
    return defaults.page_not_found(
        request, exception, template_name="patterns/pages/errors/404.html"
    )


def error_500(request):
    return defaults.server_error(
        request, template_name="patterns/pages/errors/500.html"
    )
