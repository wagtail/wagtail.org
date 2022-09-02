from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.core import blocks
from wagtail.core.blocks.struct_block import StructBlockValidationError
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

import six
from wagtailmedia.blocks import VideoChooserBlock

from wagtailio.core.choices import SVGIcon
from wagtailio.utils.blocks import CodeBlock


class PageOrExternalLinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock()
    link_text_bold = blocks.CharBlock(required=False)
    link_page = blocks.PageChooserBlock(required=False)
    # We can't use URLBlock because we may need to add an #anchor
    link_url = blocks.CharBlock(required=False)

    def clean(self, value):
        struct_value = super(PageOrExternalLinkBlock, self).clean(value)

        if not value.get("link_page") and not value.get("link_url"):
            raise ValidationError(
                "Validation error while saving block",
                params={
                    "link_url": ValidationError(
                        "You must specify link page or link url."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url."
                    ),
                },
            )

        if value.get("link_page") and value.get("link_url"):
            raise ValidationError(
                "Validation error while saving block",
                params={
                    "link_url": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                    "link_page": ValidationError(
                        "You must specify link page or link url. You can't use both."
                    ),
                },
            )

        return struct_value

    def get_context(self, value, parent_context=None):
        link_url = value.get("link_url")

        context = super(PageOrExternalLinkBlock, self).get_context(
            value, parent_context=parent_context
        )
        context.update(
            {
                "is_anchor": isinstance(link_url, six.text_type)
                and link_url.startswith("#")
            }
        )

        return context

    class Meta:
        template = "core/blocks/page_or_external_link_block.html"


class BannerBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    sub_title = blocks.CharBlock(max_length=128)
    image = ImageChooserBlock(required=False)
    video = VideoChooserBlock(required=False)
    background = ImageChooserBlock(required=False)
    links = blocks.ListBlock(PageOrExternalLinkBlock(icon="link"))

    def clean(self, value):
        errors = {}

        if not value.get("image") and not value.get("video"):
            error_message = "You must select either an image or a video."
            errors["image"] = ErrorList([error_message])
            errors["video"] = ErrorList([error_message])

        if errors:
            raise ValidationError("Validation error in StructBlock", params=errors)

        return super().clean(value)

    class Meta:
        template = "core/blocks/banner_block.html"


class BrandsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)

    # Name changed to avoid conflicts with previous revisions of pages
    brands2 = blocks.ListBlock(
        blocks.StructBlock(
            [("url", blocks.URLBlock(required=False)), ("image", ImageChooserBlock())]
        )
    )

    class Meta:
        icon = "pick"
        template = "core/blocks/brands_block.html"


class HomePageFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    all_features_page = blocks.PageChooserBlock(required=False)
    features = blocks.ListBlock(SnippetChooserBlock("features.FeatureDescription"))

    class Meta:
        template = "core/blocks/home_page_features_block.html"


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()
    image = ImageChooserBlock()
    link = blocks.URLBlock(required=False)

    class Meta:
        template = "core/blocks/testimonial_block.html"


class CodePromoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    code = CodeBlock()
    link = PageOrExternalLinkBlock()

    class Meta:
        icon = "code"
        template = "core/blocks/code_with_link_block.html"


class ShowcasesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    more_link = PageOrExternalLinkBlock(required=False)
    items = blocks.ListBlock(
        blocks.StructBlock(
            (
                ("title", blocks.CharBlock()),
                ("subtitle", blocks.CharBlock(required=False)),
                ("link_url", blocks.URLBlock(required=False)),
                ("image", ImageChooserBlock()),
            )
        )
    )

    class Meta:
        icon = "view"
        template = "core/blocks/showcases_block.html"


class PromoTextsBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    texts = blocks.ListBlock(
        blocks.StructBlock(
            (("title", blocks.CharBlock()), ("text", blocks.RichTextBlock()))
        )
    )

    class Meta:
        template = "core/blocks/promo_texts_block.html"


class HomePageBlock(blocks.StreamBlock):
    banner = BannerBlock()
    brands = BrandsBlock()
    features = HomePageFeaturesBlock()
    testimonials = blocks.ListBlock(TestimonialBlock(), icon="group")
    code = CodePromoBlock()
    showcases = ShowcasesBlock()
    promo_texts = PromoTextsBlock()

    class Meta:
        template = "core/blocks/home_page_block.html"


class CTALinkStructValue(blocks.StructValue):
    def url(self):
        cta_url = self.get("cta_url")
        cta_page = self.get("cta_page")
        return cta_url or cta_page.url


class CTALinkMixin(blocks.StructBlock):
    class Meta:
        value_class = CTALinkStructValue

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)
        if self.required and not value.get("cta_page") and not value.get("cta_url"):
            error = ErrorList(
                [ValidationError("You must specify CTA page or CTA URL.")]
            )
            errors["cta_url"] = errors["cta_page"] = error

        if value.get("cta_page") and value.get("cta_url"):
            error = ErrorList(
                [
                    ValidationError(
                        "You must specify CTA page or CTA URL. You can't use both."
                    )
                ]
            )
            errors["cta_url"] = errors["cta_page"] = error

        if not value.get("text") and (value.get("cta_page") or value.get("cta_url")):
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


class CardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    cta = CTABlock(required=False)

    class Meta:
        icon = "address-card"
        template = "patterns/components/streamfields/cards/card_block.html"
        label = "Card"


class LogoCardBlock(CTALinkMixin):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(required=False, features=["bold", "italic"])
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    logo = ImageChooserBlock(required=False)
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
    cards = blocks.ListBlock(LogoCardBlock())

    class Meta:
        template = "patterns/components/streamfields/cards/logo_cards_list_block.html"
        label = "Logo cards"


class TableContentBlock(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock(
        required=False, features=["bold", "italic", "link"]
    )
    image = ImageChooserBlock(required=False)


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
    cta = CTABlock(required=False)
    icon = blocks.ChoiceBlock(required=False, choices=SVGIcon.choices)
    dark_background = blocks.BooleanBlock(required=False, default=False)

    class Meta:
        icon = "title"
        label = "Headline"
        template = "patterns/components/streamfields/headline/headline.html"


class HighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock(required=False)
    image = ImageChooserBlock()
    image_on_right = blocks.BooleanBlock(required=False, default=False)
    meta_text = blocks.CharBlock(required=False, max_length=50)
    meta_icon = blocks.ChoiceBlock(required=False, choices=SVGIcon.choices)
    cta = CTABlock(required=False)

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
    cta = CTABlock(required=False)

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
    author_image = ImageChooserBlock(required=False)

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
    image_for_external_link = ImageChooserBlock(required=False)
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
    image = ImageChooserBlock(required=False)
    embed = EmbedBlock(required=False)
    image_on_right = blocks.BooleanBlock(required=False, default=False)
    heading = blocks.TextBlock(required=True)
    description = blocks.TextBlock(required=True)
    cta = CTABlock(required=False)

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

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        if value["page"]:
            context["value"]["url"] = value["page"].get_url
        else:
            context["value"]["url"] = value["external_link"]
        return context


class GetStartedBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    items = blocks.ListBlock(GetStartedItem(), min_num=2)

    class Meta:
        template = "patterns/components/get-started/get-started.html"


class LoopingVideoBlock(blocks.StructBlock):
    # setting autoplay to True adds 'autoplay', 'loop' & 'muted' attrs to video element
    autoplay = blocks.BooleanBlock(required=False, default=False)
    video = VideoChooserBlock()

    class Meta:
        icon = "media"
        template = "patterns/components/streamfields/looping_video_block/looping_video_block.html"


class LogoBlock(blocks.StructBlock):
    logos = blocks.ListBlock(
        ImageChooserBlock(),
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
    icon_bullets = IconBulletsBlock(icon="list-alt")
    cards = CardsBlock(icon="th-list", group="Cards")
    logo_cards = LogoCardsBlock(icon="images", group="Cards")
    cta = CTABlock(group="Call to action")
    standalone_cta = StandaloneCTABlock(group="Call to action")
    standalone_quote = StandaloneQuoteBlock(group="Quotes")
    multiple_quotes = MultipleQuoteBlock(group="Quotes")
    get_started_block = SnippetChooserBlock(
        "core.GetStartedSnippet",
        icon="th-list",
        template="patterns/components/streamfields/get_started_block/get_started_block.html",
    )
    sign_up_form = SnippetChooserBlock(
        "core.SignupFormSnippet",
        icon="envelope-open-text",
        template="patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
    )
    comparison_table = ComparisonTableBlock()

    class Meta:
        template = "patterns/components/streamfields/content_story_block.html"


class HomePageStoryBlock(blocks.StreamBlock):
    get_started_block = SnippetChooserBlock("core.GetStartedSnippet", icon="th-list")
    headline = HeadlineBlock()
    highlight = HighlightBlock()
    icon_bullets = IconBulletsBlock(icon="list-alt")
    logos = LogoBlock()
    multiple_quotes = MultipleQuoteBlock()
    standalone_cta = StandaloneCTABlock()
    teaser = TeaserBlock()
    video = LoopingVideoBlock()

    class Meta:
        template = "patterns/components/streamfields/home_page_story_block.html"
