from wagtail.wagtailcore import blocks

from wagtailio.core.blocks import PageOrExternalLinkBlock, FeatureBlock


class PrimaryFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    introduction = blocks.RichTextBlock()
    features = blocks.ListBlock(FeatureBlock())
    links = blocks.ListBlock(PageOrExternalLinkBlock())

    class Meta:
        template = 'features/blocks/primary_features_block.html'


class FeatureIndexPageBlock(blocks.StreamBlock):
    primary_features = PrimaryFeaturesBlock()

    class Meta:
        template = 'features/blocks/feature_index_page_block.html'
