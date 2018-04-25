from django import forms

from django.utils.safestring import mark_safe
from markdown import markdown
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.core.blocks import TextBlock, ChooserBlock, StructBlock, ListBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, PageChooserBlock, RawHTMLBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock


### Common Streamfield blocks ###

class BackgroundColourChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(('red', 'Red'), ('white', 'White')))


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(('left','Wrap left'),('right','Wrap right'),('mid','Mid width'),('full','Full width'),))


class SimpleImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(('left','Left'),('right','Right'),))

class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(('normal','Normal'),('full','Full width'),))


# New blocks

class ImageAndCaptionBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()


class TextAndImageBlock(StructBlock):
    text = RichTextBlock()
    image = ImageChooserBlock()
    background = BackgroundColourChoiceBlock()
    alignment = SimpleImageFormatChoiceBlock()


class BackgroundColourTextBlock(StructBlock):
    text = RichTextBlock()
    background = BackgroundColourChoiceBlock()


class CallToActionBlock(BackgroundColourTextBlock):
    pass


class TripleImageBlock(StructBlock):
    first_image = ImageChooserBlock()
    second_image = ImageChooserBlock()
    third_image = ImageChooserBlock()


class StatBlock(StructBlock):
    image = ImageChooserBlock()
    stat = CharBlock()
    text = CharBlock()

### Code and Markdown blocks https://gist.github.com/frankwiles/74a882f16704db9caa27

class CodeBlock(StructBlock):
    """
    Code Highlighting Block
    """
    LANGUAGE_CHOICES = (
        ('bash', 'Bash/Shell'),
        ('css', 'CSS'),
        ('django', 'Django templating language'),
        ('html', 'HTML'),
        ('javascript', 'Javascript'),
        ('python', 'Python'),
        ('scss', 'SCSS'),
    )

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value, context=None):
        src = value['code'].strip('\n')
        lang = value['language']

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            'html',
            linenos=None,
            cssclass='codehilite',
            style='default',
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))


class MarkDownBlock(TextBlock):
    """ MarkDown Block """

    class Meta:
        icon = 'code'

    def render_basic(self, value, context=None):
        md = markdown(
            value,
            [
                'markdown.extensions.fenced_code',
                'codehilite',
            ],
        )
        return mark_safe(md)


### Main streamfield block to be inherited by Pages ###

class StoryBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    blockquote = CharBlock(icon="openquote", classname="title")
    image = ImageChooserBlock(icon="image")
    document = DocumentChooserBlock(icon="doc-full-inverse")
    imagecaption = ImageAndCaptionBlock(label="Image caption")
    textimage = TextAndImageBlock(icon="image")
    colourtext = BackgroundColourTextBlock(icon="pilcrow")
    calltoaction = CallToActionBlock(icon="pilcrow")
    tripleimage = TripleImageBlock(icon="image")
    stats = ListBlock(StatBlock(icon="code"))
    embed = EmbedBlock(icon="code")
    markdown = MarkDownBlock()
    codeblock = CodeBlock()

    class Meta:
        template = 'core/includes/streamfield.html'
