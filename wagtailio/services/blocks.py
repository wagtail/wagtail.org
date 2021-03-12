from wagtail.core import blocks
from wagtail.core import fields


class SubheadingBlock(blocks.CharBlock):
    class Meta:
        max_length=250,
        form_classname="full",
        template="services/blocks/section_subheading.html",


class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True,  form_classname="full title")
    # TODO: Section icon
    # TODO: Section image (optional)
    # image = ImageAndCaptionBlock(required=False)
    # TODO: Section background color

    content = SectionContentBlock(required=False, form_classname="full")

    class Meta:
        icon = "cogs"
        template = "services/blocks/section.html"