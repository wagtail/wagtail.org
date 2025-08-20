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
from wagtail.documents import get_document_model
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images import get_image_model
from wagtail.images.blocks import ImageBlock
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


class CustomImageBlock(ImageBlock):
    class Meta:
        description = "An image with an alt text"
        preview_value = staticmethod(lambda: get_image_model().objects.last())


class CustomDocumentBlock(DocumentChooserBlock):
    class Meta:
        description = "A link to a document from the document library"
        preview_value = staticmethod(lambda: get_document_model().objects.last())


class CustomSnippetBlock(SnippetChooserBlock):
    def get_preview_value(self):
        return self.target_model.objects.last()


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
        label = "Code block"
        description = "A block of code with syntax highlighting"
        preview_value = {
            "language": "python",
            "code": """
class Wagtail:
    @staticmethod
    def say_hello():
        print('Hello, Wagtail!')


Wagtail.say_hello()
""".strip(),
        }

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
        return mark_safe(highlight(src, lexer, formatter))  # noqa: S308

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context["code"] = self.render_markup(context["value"])
        return context


class MarkDownBlock(TextBlock):
    """MarkDown Block"""

    class Meta:
        icon = "code"
        preview_value = (
            "The Wagtail bird is the mascot of "
            "[Wagtail](https://wagtail.org), a _free_ and **open-source** "
            "content management system (CMS) built on Django."
        )
        description = "A block of Markdown text"

    def render_markup(self, value, context=None):
        md = markdown(
            value, extensions=["markdown.extensions.fenced_code", "codehilite"]
        )
        return mark_safe(md)  # noqa: S308

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
        preview_value="The joy of heading level 2",
        description="A level 2 heading",
    )
    h3 = CharBlock(
        icon="title",
        form_classname="title",
        template="patterns/components/streamfields/headings/heading-3.html",
        preview_value="The joy of heading level 3",
        description="A level 3 heading",
    )
    h4 = CharBlock(
        icon="title",
        form_classname="title",
        template="patterns/components/streamfields/headings/heading-4.html",
        preview_value="The joy of heading level 4",
        description="A level 4 heading",
    )
    paragraph = RichTextBlock(
        icon="pilcrow",
        template="patterns/components/streamfields/rich_text_block/rich_text_block.html",
        preview_value=(
            "The Wagtail bird is the mascot of "
            '<a href="https://wagtail.org">Wagtail</a>, a <i>free</i> and '
            "<b>open-source</b> content management system (CMS) built on Django."
        ),
        description="A rich text paragraph",
    )
    blockquote = CharBlock(
        icon="openquote",
        form_classname="title",
        template="patterns/components/streamfields/quotes/standalone_quote_block.html",
        preview_value="Wagtail is such a great CMS that I love using.",
        description="A blockquote",
    )
    image = CustomImageBlock(
        icon="image", template="patterns/components/streamfields/image/image.html"
    )
    document = CustomDocumentBlock(
        icon="doc-full-inverse",
        template="patterns/components/streamfields/document/document.html",
    )
    embed = EmbedBlock(
        icon="code",
        template="patterns/components/streamfields/embed/embed.html",
        preview_value="https://www.youtube.com/watch?v=t0H1yM1FWZY",
        description="An embedded video or other media",
    )
    markdown = MarkDownBlock(
        template="patterns/components/streamfields/code_block/code_block.html"
    )
    codeblock = CodeBlock(
        template="patterns/components/streamfields/code_block/code_block.html"
    )
    teaser = TeaserBlock(group="CTA options")
    get_started_block = CustomSnippetBlock(
        "core.GetStartedSnippet",
        icon="table-list",
        template="patterns/components/streamfields/get_started_block/get_started_block.html",
        group="CTA options",
        description="A set of links to get started with Wagtail",
    )
    sign_up_form = CustomSnippetBlock(
        "core.SignupFormSnippet",
        icon="envelope-open-text",
        template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
        group="CTA options",
        description="A form to sign up for a newsletter or other service",
    )
    highlight = HighlightBlock(
        description="A block of highlighted text with a heading, description, and an optional image",
    )

    class Meta:
        template = "patterns/components/streamfields/content_story_block.html"
