from wagtail.core.blocks import (
    CharBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)


class LinkBlock(StructBlock):
    link = URLBlock(required=True)
    link_text = CharBlock(required=True)


class ContentBlock(StreamBlock):
    text = RichTextBlock()
    link_group = StreamBlock([("link", LinkBlock())])


class SectionBlock(StructBlock):
    title = CharBlock()
    content = ContentBlock()


class HomePageBlock(StreamBlock):
    section = SectionBlock()
