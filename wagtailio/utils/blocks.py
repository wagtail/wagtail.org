from django import forms

from wagtail.wagtailcore.blocks import TextBlock, ChooserBlock, StructBlock, ListBlock, StreamBlock, FieldBlock, CharBlock, RichTextBlock, PageChooserBlock, RawHTMLBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock


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


### Main streamfield block to be inherited by Pages ###

class StoryBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    image = ImageChooserBlock(icon="image")
    document = DocumentChooserBlock(icon="doc-full-inverse")
    imagecaption = ImageAndCaptionBlock(label="Image caption")
    textimage = TextAndImageBlock(icon="image")
    colourtext = BackgroundColourTextBlock(icon="pilcrow")
    calltoaction = CallToActionBlock(icon="pilcrow")
    tripleimage = TripleImageBlock(icon="image")
    stats = ListBlock(StatBlock(icon="code"))
    embed = EmbedBlock(icon="code")
