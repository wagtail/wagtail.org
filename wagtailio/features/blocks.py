from wagtail.core import blocks
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
        help_text="If left blank, 'View docs' will be used as the default Feature link title",
        default="View docs",
    )

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


class FeatureIndexPageBlock(blocks.StreamBlock):
    feature_category = FeatureCategoryBlock()

    class Meta:
        template = (
            "patterns/components/streamfields/features/feature_index_page_block.html"
        )
