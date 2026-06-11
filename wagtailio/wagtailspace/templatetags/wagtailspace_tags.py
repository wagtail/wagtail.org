from django import template

from wagtailio.wagtailspace.models import SpaceMenu


register = template.Library()


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
    url = SpaceMenu.objects.values_list("registration_url", flat=True).first()
    if url:
        return {
            "reg_url": url,
            "request": context["request"],
        }
