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


class CardBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock(required=True)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "tag"
        template = "services/blocks/card.html"


class CardsBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        child_block = CardBlock()
        super().__init__(child_block, **kwargs)

    class Meta:
        icon = "table"
        template = "services/blocks/cards.html"



class LinkButtonBlock(blocks.StructBlock):
    lead_text = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Text leading up the action text of the button.",
    )
    action_text = blocks.CharBlock(
        required=True,
        max_length=50,
        help_text="Emphasised text for the button action.",
    )
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "link"
        template = "services/blocks/link_button.html"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(required=True)
    source = blocks.CharBlock(required=True)
    reference = blocks.CharBlock(
        required=False,
        help_text=(
            "Additional information about the source. "
            "E.g. a persons job title and company."
        )
    )

    class Meta:
        icon = "openquote"
        template = "services/blocks/quote.html"


class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()
    divider = DividerBlock()
    paragraph = blocks.RichTextBlock(features=["bold", "italic", "link",  "ul", "ol"])
    cards = CardsBlock()
    link_button = LinkButtonBlock()
    quote = QuoteBlock()


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