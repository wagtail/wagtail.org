from wagtail import blocks
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
        ),
    )

    class Meta:
        icon = "openquote"
        template = "services/blocks/quote.html"


class SectionContentBlock(blocks.StreamBlock):
    subheading = SubheadingBlock()
    divider = DividerBlock()
    paragraph = blocks.RichTextBlock(features=["bold", "italic", "link", "ul", "ol"])
    cards = CardsBlock()
    link_button = LinkButtonBlock()
    quote = QuoteBlock()


class SectionMediaBlock(media_blocks.AbstractMediaChooserBlock):
    pass


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, form_classname="title")

    # Ensure that new choices are available in the icon sprite `./templates/services/includes/svg_sprite.html`
    ICON_CHOICES = [
        ("astronaut", "Astronaut"),
        ("cloud", "Cloud"),
        ("money-check", "Money check"),
        ("tools", "Tools"),
    ]
    icon = blocks.ChoiceBlock(
        choices=ICON_CHOICES,
        required=False,
    )

    section_media = SectionMediaBlock(required=False)
    section_image = image_blocks.ImageChooserBlock(
        required=False,
        help_text="Section image is used as a fallback when no media is defined.",
    )
    section_image_caption = blocks.CharBlock(
        required=False,
        label="Section image/media caption",
        help_text="Rendered below the image/media",
    )

    content = SectionContentBlock(required=False)

    class Meta:
        icon = "form"
        template = "services/blocks/section.html"
