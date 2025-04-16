from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock
from wagtail.blocks import RichTextBlock as WagtailRichTextBlock
from wagtail.images.blocks import ImageChooserBlock


NEWSLETTER_RICHTEXT_FEATURES = ["h2", "bold", "italic", "ol", "ul", "hr", "link"]


class HeadingBlock(CharBlock):
    class Meta:
        icon = "title"
        form_classname = "title"
        template = "newsletter/blocks/heading.mjml"
        label = "Heading"


class RichTextBlock(WagtailRichTextBlock):
    class Meta:
        icon = "pilcrow"
        template = "newsletter/blocks/rich_text.mjml"
        label = "Rich Text"


class AccentRichTextBlock(WagtailRichTextBlock):
    class Meta:
        icon = "pilcrow"
        template = "newsletter/blocks/accent_rich_text.mjml"
        label = "Accent Rich Text"


class ImageBlock(ImageChooserBlock):
    class Meta:
        icon = "image"
        template = "newsletter/blocks/image.mjml"
        label = "Image"


class ButtonBlock(StructBlock):
    text = CharBlock(required=True)
    url = URLBlock(required=True)

    class Meta:
        icon = "link"
        template = "newsletter/blocks/button.mjml"
        label = "Button"


class NewsletterContentBlock(StreamBlock):
    heading = HeadingBlock()
    rich_text = RichTextBlock(features=NEWSLETTER_RICHTEXT_FEATURES)
    accent_rich_text = AccentRichTextBlock(features=NEWSLETTER_RICHTEXT_FEATURES)
    image = ImageBlock()
    button = ButtonBlock()
