from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
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
