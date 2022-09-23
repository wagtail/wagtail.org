from django import template

from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtail.images.models import SourceImageIOError
from wagtail.images.templatetags.wagtailimages_tags import ImageNode

from wagtailio.blog.models import BlogPage
from wagtailio.utils.models import LinkGroupSnippet, MenuSnippet

register = template.Library()


@register.inclusion_tag("includes/menu_primary.html", takes_context=True)
def menu_primary(context, calling_page=None):
    try:
        menu = MenuSnippet.objects.get(menu_name__iexact="primary")
    except MenuSnippet.DoesNotExist:
        return {}

    links = []
    for item in menu.links.all():
        calling_page_path = calling_page.url_path if calling_page else ""
        item_path = item.link_page.url_path
        links.append(
            {
                "text": item.link_text,
                "url": pageurl(context, item.link_page),
                "active": calling_page_path.startswith(item_path)
                or calling_page_path == item_path,
            }
        )

    return {"links": links, "request": context["request"]}


@register.inclusion_tag("includes/latest_post.html", takes_context=True)
def latest_blog(context):
    post = BlogPage.objects.live().order_by("-date").first()

    return {"post": post, "request": context["request"]}


@register.inclusion_tag("includes/menu_good_to_go.html", takes_context=True)
def menu_good_to_go(context):
    try:
        menu = LinkGroupSnippet.objects.get(name__iexact="good to go")
    except LinkGroupSnippet.DoesNotExist:
        return None

    return {"links": menu.links.all(), "request": context["request"]}


@register.inclusion_tag("includes/menu_network.html", takes_context=True)
def menu_network(context):
    try:
        menu = LinkGroupSnippet.objects.get(name__iexact="network")
    except LinkGroupSnippet.DoesNotExist:
        return None

    return {"links": menu.links.all(), "request": context["request"]}


@register.filter
def carousel_next(carousel_list, current_index):
    if current_index == len(carousel_list) - 1:
        return carousel_list[0]

    return carousel_list[current_index + 1]


@register.filter
def carousel_prev(carousel_list, current_index):
    return carousel_list[current_index - 1]
