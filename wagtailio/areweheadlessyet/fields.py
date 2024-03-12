from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.models import SourceImageIOError


class ImageRenditionURLField(ImageRenditionField):
    """A field that serialises a rendition's url."""

    def to_representation(self, image):
        try:
            return image.get_rendition(self.filter_spec).full_url
        except SourceImageIOError:
            return None
