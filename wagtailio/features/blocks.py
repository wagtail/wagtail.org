from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from wagtailio.core.blocks import PageOrExternalLinkBlock


class PrimaryFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    introduction = blocks.RichTextBlock()
    features = blocks.ListBlock(SnippetChooserBlock('features.FeatureDescription'))
    links = blocks.ListBlock(PageOrExternalLinkBlock())

    class Meta:
        template = 'features/blocks/primary_features_block.html'


class AdditionalFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    features_groups = blocks.ListBlock(
        blocks.StructBlock((
            ('name', blocks.CharBlock()),
            ('features', blocks.ListBlock(
                blocks.StructBlock((
                    ('title', blocks.CharBlock()),
                    ('text', blocks.RichTextBlock()),
                ))
            )),
        ))
    )

    class Meta:
        template = 'features/blocks/additional_features_block.html'


class FeatureIndexPageBlock(blocks.StreamBlock):
    primary_features = PrimaryFeaturesBlock()
    additional_features = AdditionalFeaturesBlock()

    class Meta:
        template = 'features/blocks/feature_index_page_block.html'
