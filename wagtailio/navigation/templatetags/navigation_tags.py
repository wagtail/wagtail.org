from django import template

register = template.Library()


@register.inclusion_tag("patterns/includes/menu_footer.html", takes_context=True)
def footer_navigation(context):
    try:
        footer_navigation = context["settings"]["navigation"][
            "NavigationSettings"
        ].footer_navigation
    except (KeyError, AttributeError):
        footer_navigation = None

    return {
        "footer_navigation": footer_navigation,
    }


@register.inclusion_tag("patterns/includes/menu_main.html", takes_context=True)
def main_navigation(context):
    menus = []

    try:
        main_navigation = context["settings"]["navigation"][
            "NavigationSettings"
        ].main_navigation

        for block in main_navigation.menu_sections:
            menus.append(
                {
                    "name": block.value.get("name"),
                    "nav_items": block.value.get("nav_items"),
                    "call_to_action": block.value.get("call_to_action"),
                }
            )
    except (KeyError, AttributeError):
        return {}

    return {"menus": menus}


@register.inclusion_tag("patterns/includes/menu_get_started.html", takes_context=True)
def get_started_menu(context):
    try:
        get_started_menu = context["settings"]["navigation"][
            "NavigationSettings"
        ].get_started_menu
    except (KeyError, AttributeError):
        get_started_menu = None

    return {
        "get_started_menu": get_started_menu,
    }
