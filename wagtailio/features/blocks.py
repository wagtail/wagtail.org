from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError


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
    heading = blocks.CharBlock(max_length=255)
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
