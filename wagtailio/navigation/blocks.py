from wagtail import blocks

from wagtailio.core.blocks import CTALinkMixin
from wagtailio.core.choices import SVGIcon


# --------------- Footer Navigation ---------------


class NavLinkBlock(CTALinkMixin):
    text = blocks.CharBlock(max_length=100)
    cta_page = blocks.PageChooserBlock(label="Page", required=False)
    cta_url = blocks.URLBlock(label="URL", required=False)

    @property
    def required(self):
        return True

    class Meta:
        icon = "link"
        label = "Link"


class NavSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    links = blocks.ListBlock(NavLinkBlock())


class NavStreamField(blocks.StreamBlock):
    section = NavSectionBlock()


# --------------- Main Menu Item ---------------


class NavItemBlock(CTALinkMixin):
    text = blocks.CharBlock(label="Nav item name", max_length=55)
    short_description = blocks.CharBlock(required=False, max_length=55)
    icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    cta_page = blocks.PageChooserBlock(label="Page", required=False)
    cta_url = blocks.URLBlock(label="External Link", required=False)

    @property
    def required(self):
        return True

    class Meta:
        icon = "link"
        label = "Nav item"


class NavItemCTA(CTALinkMixin):
    text = blocks.CharBlock(label="Heading", max_length=255)
    sub_heading = blocks.CharBlock(max_length=255, required=False)
    description = blocks.CharBlock(required=False, max_length=255)
    icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    cta_page = blocks.PageChooserBlock(label="Page", required=False)
    cta_url = blocks.URLBlock(label="External Link", required=False)

    @property
    def required(self):
        return True

    class Meta:
        icon = "bullhorn"
        label = "CTA"


class MainMenuSectionBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    nav_items = blocks.ListBlock(NavItemBlock())
    call_to_action = NavItemCTA(required=False)

    class Meta:
        icon = "bars"
        label = "Main menu section"


# --------------- Wagtail Space Navigation ---------------


class SpaceMenuSectionBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=255)
    space_menu_page = blocks.PageChooserBlock(label="Page", required=False)
    space_menu_url = blocks.URLBlock(label="External Link", required=False)

    class Meta:
        icon = "bars"
        label = "Space menu section"
