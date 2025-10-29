from django.core.exceptions import ValidationError

from wagtail.blocks import (
    CharBlock,
    PageChooserBlock,
    StreamBlock,
    StructBlock,
    StructValue,
    URLBlock,
)
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


class ButtonValue(StructValue):
    @property
    def link_url(self):
        if self.get("url"):
            return self.get("url")
        elif self.get("page"):
            return self.get("page").url
        return None


class ButtonBlock(StructBlock):
    text = CharBlock(required=True)
    url = URLBlock(required=False, help_text="External URL to link to")
    page = PageChooserBlock(required=False, help_text="Internal page to link to")

    def clean(self, value):
        cleaned_data = super().clean(value)
        url = cleaned_data.get("url")
        page = cleaned_data.get("page")

        if not url and not page:
            raise ValidationError(
                "Please provide either a URL or select a page to link to."
            )

        if url and page:
            raise ValidationError("Please provide either a URL or a page, not both.")

        return cleaned_data

    class Meta:
        icon = "link"
        template = "newsletter/blocks/button.mjml"
        label = "Button"
        value_class = ButtonValue


class NewsletterContentBlock(StreamBlock):
    heading = HeadingBlock()
    rich_text = RichTextBlock(features=NEWSLETTER_RICHTEXT_FEATURES)
    accent_rich_text = AccentRichTextBlock(features=NEWSLETTER_RICHTEXT_FEATURES)
    image = ImageBlock()
    button = ButtonBlock()
