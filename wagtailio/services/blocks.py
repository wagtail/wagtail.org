from django.forms import utils
from django.utils import html

from wagtail.core import blocks
from wagtail.images import blocks as image_blocks

from wagtailmedia import blocks as media_blocks

class SubheadingBlock(blocks.CharBlock):
    class Meta:
        max_length = 250
        icon = "title"
        template = "services/blocks/subheading.html"


class DividerBlock(blocks.StaticBlock):
    class Meta:
        icon = "horizontalrule"
        admin_text = "Visual divider to differentiate between parts of content."
        template = "services/blocks/divider.html"


class CardBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock(required=True)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    link = blocks.URLBlock(required=True)
    link_text = blocks.CharBlock(required=True, default="Find out more")

    class Meta:
        icon = "tag"
        template = "services/blocks/card.html"


class CardsBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        child_block = CardBlock()
        super().__init__(child_block, **kwargs)

    class Meta:
        icon = "table"
        template = "services/blocks/cards-section.html"


class LinkButtonBlock(blocks.StructBlock):
    lead_text = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Text leading up the action text of the button.",
    )
    action_text = blocks.CharBlock(
        required=True,
        max_length=50,
        help_text="Emphasised text for the button action.",
    )
    link = blocks.URLBlock(required=True)

    class Meta:
        icon = "link"
        template = "services/blocks/link_button.html"


class QuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(required=True)
    source = blocks.CharBlock(required=True)
    reference = blocks.CharBlock(
        required=False,
        help_text=(
            "Additional information about the source. "
            "E.g. a persons job title and company."
        )
    )

    class Meta:
        icon = "openquote"
        template = "services/blocks/quote.html"


class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()
    divider = DividerBlock()
    paragraph = blocks.RichTextBlock(
        features=["bold", "italic", "link",  "ul", "ol"]
    )
    cards = CardsBlock()
    link_button = LinkButtonBlock()
    quote = QuoteBlock()


class SectionMediaBlock(media_blocks.AbstractMediaChooserBlock):
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''

        return html.format_html(player_code, html.format_html_join(
            '\n', "<source{0}>",
            [[utils.flatatt(s)] for s in value.sources]
        ))


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True,  form_classname="full title")
    icon = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text="Icon name in SVG sprite (e.g. cloud)",
    )

    section_media = SectionMediaBlock(required=False)
    section_image = image_blocks.ImageChooserBlock(required=False)
    section_image_caption = blocks.CharBlock(required=False)

    content = SectionContentBlock(required=False)

    class Meta:
        icon = "form"
        template = "services/blocks/section.html"
