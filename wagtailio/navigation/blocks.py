from wagtail.core import blocks

from wagtailio.core.blocks import CTALinkMixin


class NavLinkBlock(CTALinkMixin):
    text = blocks.CharBlock(max_length=100)
    cta_page = blocks.PageChooserBlock(label="Page", required=False)
    cta_url = blocks.URLBlock(label="URL", required=False)

    class Meta:
        icon = "link"
        label = "Link"


class NavSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    links = blocks.ListBlock(NavLinkBlock())


class NavStreamField(blocks.StreamBlock):
    section = NavSectionBlock()
