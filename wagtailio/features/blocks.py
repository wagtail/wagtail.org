from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.core import blocks
from wagtail.core.blocks.struct_block import StructBlockValidationError
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtailio.core.blocks import PageOrExternalLinkBlock


class PrimaryFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    introduction = blocks.RichTextBlock()
    features = blocks.ListBlock(SnippetChooserBlock("features.FeatureDescription"))
    links = blocks.ListBlock(PageOrExternalLinkBlock())

    class Meta:
        template = "features/blocks/primary_features_block.html"


class AdditionalFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    features_groups = blocks.ListBlock(
        blocks.StructBlock(
            (
                ("name", blocks.CharBlock()),
                (
                    "features",
                    blocks.ListBlock(
                        blocks.StructBlock(
                            (
                                ("title", blocks.CharBlock()),
                                ("text", blocks.RichTextBlock()),
                            )
                        )
                    ),
                ),
            )
        )
    )

    class Meta:
        template = "features/blocks/additional_features_block.html"


class FeatureBlock(blocks.StructBlock):
    heading = blocks.CharBlock(label="Feature heading", required=False, max_length=255)
    description = blocks.RichTextBlock(
        label="Feature description",
        required=True,
        features=["bold", "italic", "link", "document"],
    )
    link = blocks.URLBlock(label="Feature link", required=False)
    link_title = blocks.CharBlock(
        label="Feature link title",
        required=False,
        max_length=50,
        default="View docs",
    )

    def clean(self, value):
        errors = {}
        struct_value = super().clean(value)
        if value.get("link") and not value.get("link_title"):
            error = ErrorList(
                [ValidationError("You must specify a feature link title.")]
            )
            errors["link_title"] = error

        if errors:
            raise StructBlockValidationError(errors)
        return struct_value

    class Meta:
        icon = "gem"
        label = "Feature"
        template = "patterns/components/streamfields/features/feature_block.html"


class FeatureCategoryBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, max_length=255)
    features = blocks.ListBlock(FeatureBlock(), min_num=2)

    class Meta:
        icon = "folder-inverse"
        label = "Feature Category"
        template = (
            "patterns/components/streamfields/features/feature_category_block.html"
        )


class FeatureIndexStructValue(blocks.StructValue):
    def categories(self):
        blocks = self.get("blocks")
        return [block.get("heading") for block in blocks]


class FeatureIndexBlock(blocks.StructBlock):
    blocks = blocks.ListBlock(FeatureCategoryBlock())

    class Meta:
        value_class = FeatureIndexStructValue
        template = "patterns/components/streamfields/features/feature_index_block.html"
