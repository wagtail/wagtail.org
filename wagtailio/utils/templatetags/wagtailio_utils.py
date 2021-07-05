from django import template
from wagtail.core.templatetags.wagtailcore_tags import pageurl

from wagtail.images.templatetags.wagtailimages_tags import ImageNode
from wagtail.images.models import SourceImageIOError

from wagtailio.blog.models import BlogPage
from wagtailio.utils.models import MenuSnippet, LinkGroupSnippet

register = template.Library()


@register.inclusion_tag("includes/menu_primary.html", takes_context=True)
def menu_primary(context, calling_page=None):
    try:
        menu = MenuSnippet.objects.get(menu_name__iexact="primary")
    except MenuSnippet.DoesNotExist:
        return {}

    links = []
    for item in menu.links.all():
        calling_page_path = calling_page.url_path if calling_page else ''
        item_path = item.link_page.url_path
        links.append({
            "text": item.link_text,
            "url": pageurl(context, item.link_page),
            "active": calling_page_path.startswith(item_path) or calling_page_path == item_path
        })

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


# TODO: Get rid of `responsiveimage` and `ResponsiveImageNode`. It doesn't look like we use it.
@register.tag(name="responsiveimage")
def responsiveimage(parser, token):
    bits = token.split_contents()[1:]
    image_var = bits[0]
    filter_spec = bits[1]
    bits = bits[2:]

    if len(bits) == 2 and bits[0] == "as":
        # token is of the form {% image self.photo max-320x200 as img %}
        return ImageNode(image_var, filter_spec, output_var_name=bits[1])
    else:
        # token is of the form {% image self.photo max-320x200 %} - all additional tokens
        # should be kwargs, which become attributes
        attrs = {}
        for bit in bits:
            try:
                name, value = bit.split("=")
            except ValueError:
                raise template.TemplateSyntaxError(
                    "'image' tag should be of the form {% image self.photo max-320x200 [ custom-attr=\"value\" ... ] %} or {% image self.photo max-320x200 as img %}"
                )

            attrs[name] = parser.compile_filter(
                value
            )  # setup to resolve context variables as value

        return ResponsiveImageNode(image_var, filter_spec, attrs=attrs)


class ResponsiveImageNode(ImageNode, template.Node):
    def render(self, context):
        try:
            image = self.image_expr.resolve(context)
        except template.VariableDoesNotExist:
            return ""

        if not image:
            return ""

        try:
            rendition = image.get_rendition(self.filter)
        except SourceImageIOError:
            # It's fairly routine for people to pull down remote databases to their
            # local dev versions without retrieving the corresponding image files.
            # In such a case, we would get a SourceImageIOError at the point where we try to
            # create the resized version of a non-existent image. Since this is a
            # bit catastrophic for a missing image, we'll substitute a dummy
            # Rendition object so that we just output a broken link instead.
            Rendition = (
                image.renditions.model
            )  # pick up any custom Image / Rendition classes that may be in use
            rendition = Rendition(image=image, width=0, height=0)
            rendition.file.name = "not-found"

        # Parse srcset format into array
        try:
            raw_sources = str(self.attrs["srcset"]).replace('"', "").split(",")

            srcset_renditions = []
            widths = []
            newsrcseturls = []

            for source in raw_sources:
                flt = source.strip().split(" ")[0]
                width = source.strip().split(" ")[1]

                # cache widths to be re-appended after filter has been converted to URL
                widths.append(width)

                try:
                    srcset_renditions.append(image.get_rendition(flt))
                except SourceImageIOError:
                    TmpRendition = (
                        image.renditions.model
                    )  # pick up any custom Image / Rendition classes that may be in use
                    tmprend = TmpRendition(image=image, width=0, height=0)
                    tmprend.file.name = "not-found"

            for index, rend in enumerate(srcset_renditions):
                newsrcseturls.append(" ".join([rend.url, widths[index]]))

        except KeyError:
            newsrcseturls = []
            pass

        if self.output_var_name:
            # return the rendition object in the given variable
            context[self.output_var_name] = rendition
            return ""
        else:
            # render the rendition's image tag now
            resolved_attrs = {}
            for key in self.attrs:
                if key == "srcset":
                    resolved_attrs[key] = ",".join(newsrcseturls)
                    continue

                resolved_attrs[key] = self.attrs[key].resolve(context)

            return rendition.img_tag(resolved_attrs)


@register.filter
def carousel_next(carousel_list, current_index):
    if current_index == len(carousel_list) - 1:
        return carousel_list[0]

    return carousel_list[current_index + 1]


@register.filter
def carousel_prev(carousel_list, current_index):
    return carousel_list[current_index - 1]
