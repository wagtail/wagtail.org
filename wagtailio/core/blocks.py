import six
from django.core.exceptions import ValidationError
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from wagtailio.utils.blocks import CodeBlock


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


class BrandsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    brands = blocks.ListBlock(ImageChooserBlock())

    class Meta:
        template = 'core/blocks/brands_block.html'


class FeatureBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    body = blocks.StreamBlock((
        ('image', ImageChooserBlock(icon="image")),
        ('heading', blocks.CharBlock(icon="title")),
        ('paragraph', blocks.TextBlock(icon="pilcrow")),
    ), template='core/blocks/feature_block_body_block.html')


class HomePageFeaturesBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    all_features_page = blocks.PageChooserBlock(required=False)
    features = blocks.ListBlock(FeatureBlock())

    class Meta:
        template = 'core/blocks/home_page_features_block.html'


class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()
    link = blocks.URLBlock(required=False)

    class Meta:
        template = 'core/blocks/testimonial_block.html'


class CodePromoBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock(required=False)
    code = CodeBlock()
    link = SquareLinkBlock()

    class Meta:
        icon = 'code'
        template = 'core/blocks/code_with_link_block.html'


class HomeBlock(blocks.StreamBlock):
    banner = BannerBlock()
    brands = BrandsBlock()
    home_page_features = HomePageFeaturesBlock()
    testimonials = blocks.ListBlock(TestimonialBlock())
    code = CodePromoBlock()

    class Meta:
        template = 'core/blocks/home_block.html'
