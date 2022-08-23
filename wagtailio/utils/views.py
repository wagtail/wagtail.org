from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static


def favicon(request):
    try:
        favicon_path = settings.FAVICON_PATH
    except AttributeError:
        raise Http404
    return redirect(static(favicon_path), permanent=True)


def robots(request):
    content = "\n".join(["User-Agent: *", "Disallow: /search/", "Allow: /"])
    return HttpResponse(content, content_type="text/plain")


def page_not_found(request, exception):
    return render(request, "patterns/pages/errors/404.html", {})


def server_error(request, exception=None):
    return render(request, "patterns/pages/errors/500.html", {})
