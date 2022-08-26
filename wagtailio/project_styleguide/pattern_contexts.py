from pattern_library import register_context_modifier

from wagtailio.navigation.models import NavigationSettings


@register_context_modifier
def add_navigation(context, request):
    if NavigationSettings.objects.count():
        nav = NavigationSettings.objects.first()
        context["settings"] = {"navigation": {"NavigationSettings": nav}}
