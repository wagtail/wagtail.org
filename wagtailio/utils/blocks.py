from django import forms
from django.utils.safestring import mark_safe

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    FieldBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from markdown import markdown
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtailio.core.blocks import HighlightBlock, TeaserBlock

# Common Streamfield blocks


class BackgroundColourChoiceBlock(FieldBlock):  # To be removed?
    field = forms.ChoiceField(choices=(("red", "Red"), ("white", "White")))


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(
        choices=(
            ("left", "Wrap left"),
            ("right", "Wrap right"),
            ("mid", "Mid width"),
            ("full", "Full width"),
        )
    )


class SimpleImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(("left", "Left"), ("right", "Right")))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(("normal", "Normal"), ("full", "Full width")))


# Code and Markdown blocks https://gist.github.com/frankwiles/74a882f16704db9caa27


class CodeBlock(StructBlock):
    """
    Code Highlighting Block
    """

    LANGUAGE_CHOICES = (
        ("bash", "Bash/Shell"),
        ("css", "CSS"),
        ("django", "Django templating language"),
        ("html", "HTML"),
        ("javascript", "Javascript"),
        ("python", "Python"),
        ("scss", "SCSS"),
    )

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = TextBlock()

    class Meta:
        icon = "code"
        template = None

    def render_markup(self, value, context=None):
        src = value["code"].strip("\n")
        lang = value["language"]

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            "html",
            linenos=None,
            cssclass="codehilite",
            style="default",
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["code"] = self.render_markup(context["value"])
        return context


class MarkDownBlock(TextBlock):
    """MarkDown Block"""

    class Meta:
        icon = "code"

    def render_markup(self, value, context=None):
        md = markdown(
            value, extensions=["markdown.extensions.fenced_code", "codehilite"]
        )
        return mark_safe(md)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["code"] = self.render_markup(context["value"])
        return context


# Main streamfield block to be inherited by Pages


class StoryBlock(StreamBlock):
    h2 = CharBlock(
        icon="title",
        form_classname="title",
        template="patterns/components/streamfields/headings/heading-2.html",
    )
    h3 = CharBlock(
        icon="title",
        form_classname="title",
        template="patterns/components/streamfields/headings/heading-3.html",
    )
    h4 = CharBlock(
        icon="title",
        form_classname="title",
        template="patterns/components/streamfields/headings/heading-4.html",
    )
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="patterns/components/streamfields/rich_text_block/rich_text_block.html",
    )
    blockquote = CharBlock(
        icon="openquote",
        form_classname="title",
        template="patterns/components/streamfields/quotes/standalone_quote_block.html",
    )
    image = ImageChooserBlock(
        icon="image", template="patterns/components/streamfields/image/image.html"
    )
    document = DocumentChooserBlock(
        icon="doc-full-inverse",
        template="patterns/components/streamfields/document/document.html",
    )
    embed = EmbedBlock(
        icon="code", template="patterns/components/streamfields/embed/embed.html"
    )
    markdown = MarkDownBlock(
        template="patterns/components/streamfields/code_block/code_block.html"
    )
    codeblock = CodeBlock(
        template="patterns/components/streamfields/code_block/code_block.html"
    )
    teaser = TeaserBlock(group="CTA options")
    get_started_block = SnippetChooserBlock(
        "core.GetStartedSnippet",
        icon="th-list",
        template="patterns/components/streamfields/get_started_block/get_started_block.html",
        group="CTA options",
    )
    sign_up_form = SnippetChooserBlock(
        "core.SignupFormSnippet",
        icon="envelope-open-text",
        template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
        group="CTA options",
    )
    highlight = HighlightBlock()

    class Meta:
        template = "patterns/components/streamfields/content_story_block.html"
