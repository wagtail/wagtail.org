from django import template

register = template.Library()


@register.inclusion_tag("patterns/includes/menu_footer.html", takes_context=True)
def footer_navigation(context, block):
    request = context["request"]
    return {
        "footer_navigation": context["settings"]["navigation"][
            "NavigationSettings"
        ].footer_navigation,
        "request": request,
    }
