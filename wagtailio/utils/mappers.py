from wagtail_content_import.mappers.converters import (
    ImageConverter,
    RichTextConverter,
    # TableConverter,
    TextConverter,
)
import base64
import re
from wagtail_content_import.mappers.streamfield import (
    StreamFieldMapper as _StreamFieldMapper,
)


class DocxImageConverter(ImageConverter):
    src_data_finder = re.compile("base64,(.*)")

    def __call__(self, element, user, **kwargs):
        src_data = self.src_data_finder.search(element["value"])
        if src_data:
            image_content = base64.b64decode(src_data.group(1))
            image_name = "imported-image"
        else:
            image_name, image_content = self.fetch_image(element["value"])
        title = element.get("title", "")
        image = self.import_as_image_model(
            image_name, image_content, owner=user, title=title
        )
        return (self.block_name, image)


class StreamFieldMapper(_StreamFieldMapper):
    html = RichTextConverter("paragraph")
    image = DocxImageConverter("image")
    heading = TextConverter("h2")
    # table = TableConverter('')
