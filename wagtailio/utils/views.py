from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.templatetags.static import static


def favicon(request):
    try:
        favicon_path = settings.FAVICON_PATH
    except AttributeError:
        raise Http404
    return redirect(static(favicon_path), permanent=True)
