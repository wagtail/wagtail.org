from django.conf import settings
from django.http import JsonResponse
from django.utils.cache import patch_cache_control

from wagtail.core.models import Site
from wagtail.core.rich_text import expand_db_html

from .models import SiteWideAlertSettings


def sitewide_alert(request):
    site = Site.find_for_request(request)
    alert_settings = SiteWideAlertSettings.for_site(site)
    data = {}
    if alert_settings.sitewide_alert_enabled:
        data = {
            "text": expand_db_html(alert_settings.sitewide_alert_text),
        }
        if alert_settings.background_colour:
            data["bg_colour"] = alert_settings.background_colour
        if alert_settings.text_colour:
            data["text_colour"] = alert_settings.text_colour

    response = JsonResponse(data)

    # Browser should cache only briefly
    max_age = getattr(settings, "SITEWIDE_ALERT_MAXAGE", 300)
    # FE cache can cache indefinitely, as will be purged on change
    s_maxage = getattr(settings, "SITEWIDE_ALERT_SMAXAGE", 604800)
    patch_cache_control(response, max_age=max_age, s_maxage=s_maxage, public=True)
    return response
