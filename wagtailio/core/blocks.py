from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtailmedia.blocks import VideoChooserBlock

from wagtailio.core.choices import SVGIcon


class CTALinkStructValue(blocks.StructValue):
    def url(self):
        if cta_url := self.get("cta_url"):
            return cta_url

        if cta_page := self.get("cta_page"):
            return cta_page.url

        return ""


class CTALinkMixin(blocks.StructBlock):
    class Meta:
        value_class = CTALinkStructValue

    def clean(self, value):
        struct_value = super().clean(value)

        errors = {}
        url = value.get("cta_url")
        page = value.get("cta_page")
        if self.required and not page and not url:
            error = ErrorList(
                [ValidationError("You must specify CTA page or CTA URL.")]
            )
            errors["cta_url"] = errors["cta_page"] = error

        if page and url:
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify CTA page or CTA URL. You can't use both."
                    )
                ]
            )
            errors["cta_url"] = errors["cta_page"] = error

        if not value.get("text") and (page or url):
            error = ErrorList([ValidationError("You must specify CTA text.")])
            errors["text"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if value["cta_url"]:
            context["value"]["url"] = value["cta_url"]
        if value["cta_page"]:
            context["value"]["url"] = value["cta_page"].get_url
        return context


class CTABlock(CTALinkMixin):
    text = blocks.CharBlock(label="CTA text", max_length=255, required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    @property
    def required(self):
        return True

    class Meta:
        icon = "bullhorn"
        template = "patterns/components/streamfields/cta/cta_block.html"
        label = "CTA"


class OptionalCTABlock(CTABlock):
    @property
    def required(self):
        return False


class CardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    cta = OptionalCTABlock()

    class Meta:
        icon = "address-card"
        template = "patterns/components/streamfields/cards/card_block.html"
        label = "Card"


class LogoCardBlock(CTALinkMixin):
    text = blocks.CharBlock(label="Heading", max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    logo = ImageBlock(required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    class Meta:
        icon = "image"
        template = "patterns/components/streamfields/cards/logo_card_block.html"
        label = "Logo card"


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardBlock())

    class Meta:
        template = "patterns/components/streamfields/cards/cards_list_block.html"
        label = "Cards"


class LogoCardsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    cards = blocks.ListBlock(LogoCardBlock())

    class Meta:
        template = "patterns/components/streamfields/cards/logo_cards_list_block.html"
        label = "Logo cards"


class TableContentBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock(
        required=False, features=["bold", "italic", "link"]
    )
    image = ImageBlock(required=False)


class ComparisonTableBlock(blocks.StructBlock):
    comparison_table = TypedTableBlock(
        [
            ("content", TableContentBlock(max_num=1, required=False)),
        ],
    )

    class Meta:
        icon = "table"
        template = "patterns/components/streamfields/comparison_table_block/comparison_table_block.html"


class HeadlineBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    sub_heading = blocks.TextBlock(required=False)
    intro = blocks.TextBlock(required=False)
    cta = OptionalCTABlock()
    icon = blocks.ChoiceBlock(required=False, choices=SVGIcon.choices)
    dark_background = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = "title"
        label = "Headline"
        template = "patterns/components/streamfields/headline/headline.html"


class HighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock(required=False)
    image = ImageBlock()
    image_on_right = blocks.BooleanBlock(required=False, default=False)
    meta_text = blocks.CharBlock(required=False, max_length=50)
    meta_icon = blocks.ChoiceBlock(required=False, choices=SVGIcon.choices)
    cta = OptionalCTABlock()

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        # meta_icon goes together with meta_text
        sum_meta_values = bool(value.get("meta_text")) + bool(value.get("meta_icon"))

        if sum_meta_values == 1:
            error = ErrorList(
                [
                    ValidationError(
                        "meta icon goes hand-in-hand with meta text, you cannot specify one without the other"
                    )
                ]
            )
            errors["meta_text"] = errors["meta_icon"] = error

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if value["image_on_right"]:
            context["image_on_right"] = value["image_on_right"]
        return context

    class Meta:
        icon = "newspaper"
        label = "Highlight"
        template = (
            "patterns/components/streamfields/highlight_block/highlight_block.html"
        )


class IconBulletBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "link"],
    )
    cta = OptionalCTABlock()

    class Meta:
        icon = "tick-inverse"
        label = "Icon bullet"
        template = (
            "patterns/components/streamfields/icon_bullet_block/icon_bullet_block.html"
        )


class IconBulletsBlock(blocks.StructBlock):
    icon_bullets = blocks.ListBlock(IconBulletBlock())

    class Meta:
        template = "patterns/components/streamfields/icon_bullets_list_block/icon_bullets_list_block.html"
        label = "Icon bullets"


class StandaloneQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    author = blocks.RichTextBlock(
        required=True,
        features=["link"],
    )
    author_image = ImageBlock(required=False)

    class Meta:
        icon = "openquote"
        label = "Standalone quote"
        template = "patterns/components/streamfields/quotes/standalone_quote_block.html"


class MultipleQuoteBlock(blocks.StructBlock):
    heading = blocks.TextBlock(required=True)
    quotes = blocks.ListBlock(StandaloneQuoteBlock(), min_num=2)

    class Meta:
        icon = "openquote"
        label = "Multiple quotes"
        template = "patterns/components/streamfields/quotes/quotes.html"


class RichTextBlock(blocks.StructBlock):
    rich_text = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "h2", "h3", "ol", "ul", "link", "document"],
    )

    class Meta:
        icon = "bold"
        label = "Rich text"
        template = (
            "patterns/components/streamfields/rich_text_block/rich_text_block.html"
        )


class StandaloneCTABlock(blocks.StructBlock):
    cta = CTABlock()
    description = blocks.TextBlock(
        label="Short description", required=False, max_length=100
    )

    class Meta:
        icon = "bullhorn"
        label = "Standalone CTA"
        template = "patterns/components/streamfields/cta/cta.html"


class TeaserBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False, page_type=["blog.BlogPage"])
    url_chooser = blocks.URLBlock(required=False)
    image_for_external_link = ImageBlock(required=False)
    heading_for_external_link = blocks.TextBlock(required=False)
    subheading_for_ext_link = blocks.TextBlock(
        label="Subheading for external link", required=False
    )

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        # We want the logical AND of three values
        sum_external_link_values = (
            bool(value.get("image_for_external_link"))
            + bool(value.get("heading_for_external_link"))
            + bool(value.get("subheading_for_ext_link"))
        )

        if not value.get("page") and not value.get("url_chooser"):
            error = ErrorList([ValidationError("You must specify a page or a URL.")])
            errors["page"] = errors["url_chooser"] = error

        if value.get("page") and value.get("url_chooser"):
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify a page or a URL. You can't use both."
                    )
                ]
            )
            errors["page"] = errors["url_chooser"] = error

        if value.get("url_chooser") and sum_external_link_values < 3:
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify an image, heading and subheading for the external URL."
                    )
                ]
            )
            errors["image_for_external_link"] = errors[
                "heading_for_external_link"
            ] = errors["subheading_for_ext_link"] = error

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "gem"
        label = "Teaser"
        template = "patterns/components/streamfields/teaser_block/teaser_block.html"


class TextAndMediaBlock(blocks.StructBlock):
    image = ImageBlock(required=False)
    embed = EmbedBlock(required=False)
    image_on_right = blocks.BooleanBlock(required=False, default=False)
    heading = blocks.TextBlock(required=True)
    description = blocks.TextBlock(required=True)
    cta = OptionalCTABlock()

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        if not value.get("image") and not value.get("embed"):
            error = ErrorList([ValidationError("You must specify Image or Embed.")])
            errors["image"] = errors["embed"] = error

        if value.get("embed") and value.get("image"):
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify Image or Embed. You can't use both."
                    )
                ]
            )
            errors["image"] = errors["embed"] = error

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "media"
        label = "Text and Media"
        template = "patterns/components/streamfields/text_and_media_block/text_and_media_block.html"


class GetStartedItem(blocks.StructBlock):
    """This is meant to be used as part of GetStartedBlock"""

    heading = blocks.CharBlock(max_length=255)
    subheading = blocks.CharBlock(max_length=255)
    description = blocks.TextBlock()
    icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    page = blocks.PageChooserBlock(required=False)
    external_link = blocks.URLBlock(required=False)

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        if not value.get("page") and not value.get("external_link"):
            error = ErrorList([ValidationError("You must specify a page or a URL.")])
            errors["page"] = errors["external_link"] = error

        if value.get("page") and value.get("external_link"):
            error = ErrorList(
                [ValidationError("You must specify a page or URL. You can't use both.")]
            )
            errors["external_link"] = errors["page"] = error

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        template = "patterns/components/icon-link/icon-link.html"


class GetStartedBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255, required=False)
    items = blocks.ListBlock(GetStartedItem(), min_num=2)

    class Meta:
        template = "patterns/components/get-started/get-started.html"


class VideoBlock(blocks.StructBlock):
    # setting autoplay to True adds 'autoplay', 'loop' & 'muted' attrs to video element
    heading = blocks.CharBlock(required=False)
    video = VideoChooserBlock(required=False)
    embed = EmbedBlock(required=False)

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        if not value.get("video") and not value.get("embed"):
            error = ErrorList(
                [ValidationError("You must specify a video or embedded video.")]
            )
            errors["video"] = errors["embed"] = error

        if value.get("embed") and value.get("video"):
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify a self-hosted video or embedded video. You can't use both."
                    )
                ]
            )
            errors["video"] = errors["embed"] = error

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "media"
        template = "patterns/components/streamfields/video_block/video_block.html"


class LogoBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    logos = blocks.ListBlock(
        ImageBlock(),
    )

    class Meta:
        icon = "images"
        template = "patterns/components/streamfields/logo_block/logo_block.html"


class ContentStoryBlock(blocks.StreamBlock):
    rich_text = RichTextBlock()
    text_and_media = TextAndMediaBlock()
    headline = HeadlineBlock()
    highlight = HighlightBlock()
    teaser = TeaserBlock()
    icon_bullets = IconBulletsBlock(icon="rectangle-list")
    cards = CardsBlock(icon="table-list", group="Cards")
    logo_cards = LogoCardsBlock(icon="images", group="Cards")
    cta = CTABlock(group="Call to action")
    standalone_cta = StandaloneCTABlock(group="Call to action")
    standalone_quote = StandaloneQuoteBlock(group="Quotes")
    multiple_quotes = MultipleQuoteBlock(group="Quotes")
    get_started_block = SnippetChooserBlock(
        "core.GetStartedSnippet",
        icon="table-list",
        template="patterns/components/streamfields/get_started_block/get_started_block.html",
    )
    sign_up_form = SnippetChooserBlock(
        "core.SignupFormSnippet",
        icon="envelope-open-text",
        template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
    )
    comparison_table = ComparisonTableBlock()
    logos = LogoBlock(group="Logos")
    video = VideoBlock()

    class Meta:
        template = "patterns/components/streamfields/content_story_block.html"


class HomePageStoryBlock(blocks.StreamBlock):
    get_started_block = SnippetChooserBlock("core.GetStartedSnippet", icon="th-list")
    headline = HeadlineBlock()
    highlight = HighlightBlock()
    icon_bullets = IconBulletsBlock(icon="rectangle-list")
    logos = LogoBlock()
    multiple_quotes = MultipleQuoteBlock()
    standalone_cta = StandaloneCTABlock()
    teaser = TeaserBlock()
    video = VideoBlock()

    class Meta:
        template = "patterns/components/streamfields/home_page_story_block.html"

class SpaceStoryBlock(blocks.StreamBlock): 
    rich_text = RichTextBlock()
    heading = blocks.RichTextBlock(
        required=False,
        features=["bold", "italic", "h2", "h3", "link"],
    )
    image = ImageBlock(required=False)
    class Meta:
        template = "patterns/components/streamfields/space_story_block.html"


