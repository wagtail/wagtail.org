import six
from django.core.exceptions import ValidationError
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock


class SquareLinkBlock(blocks.StructBlock):
    link_text = blocks.CharBlock()
    link_text_bold = blocks.CharBlock(required=False)
    link_page = blocks.PageChooserBlock(required=False)
    # We can't use URLBlock because we may need to add an #anchor
    link_url = blocks.CharBlock(required=False)

    def clean(self, value):
        struct_value = super(SquareLinkBlock, self).clean(value)

        if not value.get('link_page') and not value.get('link_url'):
            raise ValidationError("Validation error while saving block", params={
                'link_url': ValidationError("You must specify link page or link url."),
                'link_page': ValidationError("You must specify link page or link url."),
            })

        if value.get('link_page') and value.get('link_url'):
            raise ValidationError("Validation error while saving block", params={
                'link_url': ValidationError("You must specify link page or link url. You can't use both."),
                'link_page': ValidationError("You must specify link page or link url. You can't use both."),
            })

        return struct_value

    def get_context(self, value):
        link_url = value.get('link_url')

        context = super(SquareLinkBlock, self).get_context(value)
        context.update({
            'is_anchor': isinstance(link_url, six.text_type) and link_url.startswith('#')
        })

        return context

    class Meta:
        template = 'core/blocks/square_link_block.html'


class BannerBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=128)
    sub_title = blocks.CharBlock(max_length=128)
    image = ImageChooserBlock()
    background = ImageChooserBlock(required=False)
    links = blocks.ListBlock(SquareLinkBlock())

    class Meta:
        template = 'core/blocks/banner_block.html'


# Main streamfield block to be inherited by Pages

class HomeBlock(blocks.StreamBlock):
    banner = BannerBlock()
