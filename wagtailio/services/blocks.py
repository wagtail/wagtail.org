from wagtail.core import blocks
from wagtail.core import fields


class SubheadingBlock(blocks.CharBlock):
    class Meta:
        max_length = 250
        icon = "title"
        form_classname = "full"
        template = "services/blocks/subheading.html"


class DividerBlock(blocks.StaticBlock):
    class Meta:
        icon = "horizontalrule"
        admin_text = "Visual divider to differentiate between parts of content."
        template = "services/blocks/divider.html"


class ParagraphBlock(blocks.RichTextBlock):

    def __init__(self, **kwargs):
        super().__init__(features=["bold", "italic", "link",  "ul", "ol"], **kwargs)
    class Meta:
        icon = "pilcrow"

class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()
    divider = DividerBlock()
    paragraph = ParagraphBlock()


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True,  form_classname="full title")
    # TODO: Section icon
    # TODO: Section image (optional)
    # image = ImageAndCaptionBlock(required=False)
    # TODO: Section background color

    content = SectionContentBlock(required=False, form_classname="full")

    class Meta:
        icon = "form"
        template = "services/blocks/section.html"