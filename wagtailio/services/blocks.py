from wagtail.core import blocks
from wagtail.core import fields


class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)

    class Meta:
        icon = "cogs"