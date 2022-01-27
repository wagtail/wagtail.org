from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
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


class NewsBlock(StreamBlock):
    blog_post = PageChooserBlock(page_type="blog.BlogPage")

    class Meta:
        max_num = 3


class HomePageBlock(StreamBlock):
    section = SectionBlock()
    news = NewsBlock()
    topics = StructBlock([("title", CharBlock())])

    class Meta:
        block_counts = {
            "news": {"max_num": 1},
            "topics": {"max_num": 1},
        }


class TopicPageBlock(StreamBlock):
    text = RichTextBlock()
    section = SectionBlock()
    news = NewsBlock()

    class Meta:
        block_counts = {"news": {"max_num": 1}}
