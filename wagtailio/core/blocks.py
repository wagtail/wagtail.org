from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

import six
from wagtailmedia.blocks import VideoChooserBlock

from wagtailio.utils.blocks import CodeBlock
from wagtailio.utils.models import SVGIcon


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
        struct_value = super(PageOrExternalLinkBlock, self).clean(value)

        if not value.get("cta_page") and not value.get("cta_url"):
            raise ValidationError(
                "Validation error while saving block",
                params={
                    "cta_url": ValidationError(
                        "You must specify CTA page or CTA URL."
                    ),
                    "cta_page": ValidationError(
                        "You must specify CTA page or CTA URL."
                    ),
                },
            )

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
        icon = "tick-inverse"
        # template = "" # TODO: add template
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
        # template = "" # TODO: add template
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
        # template = "" # TODO: add template
        label = "Logo card"


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(CardBlock())

    class Meta:
        # template = "" # TODO: add template
        label = "Cards"


class LogoCardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(LogoCardBlock())


    class Meta:
        # template = "" # TODO: add template
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
        template = ""  # TODO: add template


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
        template = ""  # TODO: add template
