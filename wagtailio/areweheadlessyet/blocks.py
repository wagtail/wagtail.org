from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.snippets.blocks import SnippetChooserBlock


class LinkBlock(StructBlock):
    link = URLBlock(required=True)
    link_text = CharBlock(required=True)


class ContentBlock(StreamBlock):
    text = RichTextBlock()
    link_group = StreamBlock([("link", LinkBlock())])


class SectionBlock(StructBlock):
    title = CharBlock()
    content = ContentBlock()


class BlogPostChooserBlock(PageChooserBlock):
    def get_api_representation(self, value, context=None):
        if value is None:
            return None
        return {
            "date": value.date,
            "title": value.title,
            "url": value.full_url,
            "introduction": value.introduction,
        }


class BlogPostsBlock(StreamBlock):
    blog_post = BlogPostChooserBlock(page_type="blog.BlogPage")

    class Meta:
        max_num = 3


class NewsBlock(StructBlock):
    title = CharBlock()
    blog_posts = BlogPostsBlock()


class IssueChooserBlock(SnippetChooserBlock):
    def get_api_representation(self, value, context=None):
        if value is None:
            return None
        return {"title": value.title, "url": value.url}


class IssuesBlock(StructBlock):
    title = CharBlock()
    summary = CharBlock(required=False)
    issues = StreamBlock(
        [("issue", IssueChooserBlock("areweheadlessyet.WagtailHeadlessIssue"))]
    )


class HomePageBlock(StreamBlock):
    section = SectionBlock()
    news = NewsBlock()
    topics = StructBlock([("title", CharBlock())])
    issues = IssuesBlock()

    class Meta:
        block_counts = {
            "news": {"max_num": 1},
            "topics": {"max_num": 1},
            "issues": {"max_num": 1},
        }


class TopicPageBlock(StreamBlock):
    text = RichTextBlock()
    section = SectionBlock()
    news = NewsBlock()

    class Meta:
        block_counts = {"news": {"max_num": 1}}
