from wagtail.core import blocks
from wagtail.core import fields
from wagtail.images import blocks as image_blocks


class SubheadingBlock(blocks.CharBlock):
    class Meta:
        max_length = 250
        icon = "title"
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


class CardTextBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        super().__init__(features=["bold", "italic"], **kwargs)
    class Meta:
        icon = "pilcrow"


class CardBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock(required=True)
    text = CardTextBlock(required=True)
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "tag"
        template = "services/blocks/card.html"

class CardsSectionBlock(blocks.StreamBlock):
    card = CardBlock()

    class Meta:
        icon = "table"
        template = "services/blocks/cards_section.html"


class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()
    divider = DividerBlock()
    paragraph = ParagraphBlock()
    card_section = CardsSectionBlock()


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True,  form_classname="full title")
    # TODO: Section icon
    # TODO: Section image (optional)
    # image = ImageAndCaptionBlock(required=False)
    # TODO: Section background color

    content = SectionContentBlock(required=False)

    class Meta:
        icon = "form"
        template = "services/blocks/section.html"