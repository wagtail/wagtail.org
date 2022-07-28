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

from wagtailio.utils.blocks import CodeBlock
from wagtailio.utils.choices import SVGIcon


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


class CTABlock(blocks.StructBlock):
    cta_text = blocks.CharBlock(label="CTA text", max_length=255)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)

        if not value.get("cta_page") and not value.get("cta_url"):
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify CTA page or CTA URL."
                    )
                ]
            )
            errors["cta_url"] = errors["cta_page"] = e

        if value.get("cta_page") and value.get("cta_url"):
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify CTA page or CTA URL. You can't use both."
                    )
                ]
            )
            errors["cta_url"] = errors["cta_page"] = e

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "tick-inverse"
        template = "patterns/components/streamfield/cta_block.html"
        label = "CTA"


class CardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(
        required=False, features=["bold", "italic"]
    )
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    cta = CTABlock(required=False)

    class Meta:
        icon = "placeholder"
        template = "patterns/components/streamfield/card_block.html"
        label = "Card"


class LogoCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=255)
    description = blocks.RichTextBlock(
        required=False, features=["bold", "italic"]
    )
    meta_icon = blocks.ChoiceBlock(choices=SVGIcon.choices)
    meta_text = blocks.TextBlock(max_length=50)
    logo = ImageChooserBlock(required=False)
    cta_page = blocks.PageChooserBlock(label="CTA page", required=False)
    cta_url = blocks.URLBlock(label="CTA URL", required=False)

    def clean(self, value):
        struct_value = super(PageOrExternalLinkBlock, self).clean(value)

        if value.get("cta_page") and value.get("cta_url"):
            raise ValidationError(
                "Validation error while saving block",
                params={
                    "cta_url": ValidationError(
                        "You must specify CTA page or CTA URL. You can't use both."
                    ),
                    "cta_page": ValidationError(
                        "You must specify CTA page or CTA URL. You can't use both."
                    ),
                },
            )

        return struct_value

    class Meta:
        icon = "placeholder"
        template = "patterns/components/streamfield/logo_card_block.html"
        label = "Logo card"


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardBlock())

    class Meta:
        template = "patterns/components/streamfield/cards_list_block.html"
        label = "Cards"


class LogoCardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(LogoCardBlock())


    class Meta:
        template = "patterns/components/streamfield/logo_cards_list_block.html"
        label = "Logo cards"


class ComparisonTableBlock(blocks.StructBlock):
    comparison_table = TypedTableBlock([
        ('rich_text', blocks.RichTextBlock(features=["bold", "italic", "link"])),
        ('image', ImageChooserBlock()),
    ])

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context)

        rows = []
        columns = next(ctx["value"]["table"].rows, [])
        num_rows = 0

        for column_data in columns:
            # column_data.value contains the cells of a single column
            block_name = column_data.block.name
            curr_row = 0
            for row_data in column_data.value:
                if num_rows <= curr_row:
                    rows.append([])
                    num_rows += 1
                rows[curr_row].append({"block_name": block_name, "value": row_data})
                curr_row += 1

        ctx["value"]["rows"] = rows
        return ctx

    class Meta:
        icon = "table"
        template = "patterns/components/streamfield/comparison_table_block.html"


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
        template = "patterns/components/streamfield/headline_block.html"


class HighlightBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=100)
    description = blocks.TextBlock(required=False)
    image = ImageChooserBlock()
    image_on_right = blocks.BooleanBlock(required=False, default=False)
    meta_text = blocks.CharBlock(required=False, max_length=50)
    meta_icon = blocks.ChoiceBlock(required=False, choices=SVGIcon.choices)
    cta = CTABlock(required=False)

    class Meta:
        icon = "placeholder"
        label = "Highlight"
        template = "patterns/components/streamfield/highlight_block.html"


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
        template = "patterns/components/streamfield/icon_bullet_block.html"


class IconBulletsBlock(blocks.StructBlock):
    icon_bullet = blocks.ListBlock(IconBulletBlock())

    class Meta:
        template = "patterns/components/streamfield/icon_bullets_list_block.html"
        label = "Icon bullets"


class StandaloneQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    author = blocks.RichTextBlock(
        required=True,
        features=[
            "bold",
            "italic",
            "h2",
            "h3",
            "h4",
            "h5",
            "ol",
            "ul",
            "link",
            "image",
            "document",
            "embed",
        ],
    )
    author_image = ImageChooserBlock(required=False)

    class Meta:
        icon = "openquote"
        label = "Standalone quote"
        template = "patterns/components/streamfield/standalone_quote_block.html"


class MultipleQuoteBlock(blocks.StructBlock):
    heading = blocks.TextBlock(required=True)
    quotes = blocks.ListBlock(StandaloneQuoteBlock(), min_num=2)

    class Meta:
        icon = "openquote"
        label = "Multiple quotes"
        template = "patterns/components/streamfield/multiple_quotes_block.html"


class RichTextBlock(blocks.StructBlock):
    rich_text = blocks.RichTextBlock(
        required=True,
        features=["bold", "italic", "h2", "h3", "ol", "ul", "link", "document"],
    )

    class Meta:
        icon = "bold"
        label = "Rich text"
        template = "patterns/components/streamfield/rich_text_block.html"

class StandaloneCTABlock(blocks.StructBlock):
    short_description = blocks.TextBlock(required=False, max_length=100)
    cta = CTABlock()

    class Meta:
        icon = "arrow-right"
        label = "Standalone CTA"
        template = "patterns/components/streamfield/standalone_cta_block.html"


class TeaserBlock(blocks.StructBlock):
    blog_post_chooser = blocks.PageChooserBlock(required=False, page_type=["blog.BlogPage"])
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

        if not value.get("blog_post_chooser") and not value.get("url_chooser"):
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify a blog post or a URL."
                    )
                ]
            )
            errors["blog_post_chooser"] = errors["url_chooser"] = e

        if value.get("blog_post_chooser") and value.get("url_chooser"):
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify a blog post or a URL. You can't use both."
                    )
                ]
            )
            errors["blog_post_chooser"] = errors["url_chooser"] = e

        if value.get("url_chooser") and sum_external_link_values < 3:
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify an image, heading and subheading for the external URL."
                    )
                ]
            )
            errors["image_for_external_link"] = errors["heading_for_external_link"] = errors["subheading_for_ext_link"] = e

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "placeholder"
        label = "Teaser"
        template = "patterns/components/streamfield/teaser_block.html"


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
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify Image or Embed."
                    )
                ]
            )
            errors["image"] = errors["embed"] = e

        if value.get("embed") and value.get("image"):
            e = ErrorList(
                [
                    ValidationError(
                        "You must specify Image or Embed. You can't use both."
                    )
                ]
            )
            errors["image"] = errors["embed"] = e

        if errors:
            raise StructBlockValidationError(errors)

        return struct_value

    class Meta:
        icon = "media"
        label = "Text and Media"
        template = "patterns/components/streamfield/text_and_media_block.html"
