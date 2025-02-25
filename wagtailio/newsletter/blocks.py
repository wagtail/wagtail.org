from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class HeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(help_text="The heading text")
    size = blocks.ChoiceBlock(
        choices=[
            ("h2", "H2"),
            ("h3", "H3"),
        ],
        default="h2",
    )

    class Meta:
        icon = "title"
        template = "newsletter/blocks/heading_block.html"


class CallToActionBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    url = blocks.URLBlock()
    button_text = blocks.CharBlock()

    class Meta:
        icon = "link"
        template = "newsletter/blocks/cta_block.html"


class TextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock()
    theme = blocks.ChoiceBlock(
        choices=[
            ("white", "White"),
            ("purple", "Purple"),
        ],
        default="white",
    )

    class Meta:
        icon = "doc-full"
        template = "newsletter/blocks/text_block.html"


class NewsletterStoryBlock(blocks.StreamBlock):
    heading = HeadingBlock()
    text = TextBlock()
    image = ImageBlock()
    cta = CallToActionBlock()
