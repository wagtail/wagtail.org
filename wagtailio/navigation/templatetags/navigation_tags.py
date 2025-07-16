from django import template

from wagtailio.navigation.models import SpaceMenu


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


@register.inclusion_tag("patterns/includes/space_main.html", takes_context=True)
def space_navigation(context):
    spacemenus = []

    try:
        space_navigation = context["settings"]["navigation"][
            "NavigationSettings"
        ].space_navigation

        for block in space_navigation.menu_sections:
            spacemenus.append(
                {
                    "name": block.value.get("name"),
                    "menu_page": block.value.get("space_menu_page"),
                    "menu_url": block.value.get("space_menu_url"),
                }
            )
    except (KeyError, AttributeError):
        return {}

    return {"spacemenus": spacemenus}


@register.inclusion_tag(
    "patterns/components/buttons/spacereg-button.html", takes_context=True
)
def get_reg_url(context):
    if space_menu := SpaceMenu.objects.first():
        return {
            "reg_url": space_menu,
            "request": context["request"],
        }


# TODO: Fix this template tag to grab registration URL from the SpaceMenu model
