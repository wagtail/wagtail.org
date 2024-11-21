from wagtail.images.blocks import ImageBlock


def to_python_with_default_alt(self, value):
    # For backward compatibility with ImageChooserBlock
    if value is None or isinstance(value, int):
        image = self.child_blocks["image"].to_python(value)
        struct_value = {
            "image": image,
            "decorative": False,
            "alt_text": (
                image.default_alt_text if image else ""
            ),  # THIS IS THE ONLY CHANGE
        }
    else:
        struct_value = super(ImageBlock, self).to_python(value)
    return self._struct_value_to_image(struct_value)


def bulk_to_python_with_default_alt(self, values):
    values = list(values)

    if values and all(value is None or isinstance(value, int) for value in values):
        # `values` looks like a list of image IDs and/or None values (as we might encounter
        # if an ImageChooserBlock has been changed to an ImageBlock with no data migration)
        image_values = self.child_blocks["image"].bulk_to_python(values)

        struct_values = [
            {
                "image": image,
                "decorative": False,
                "alt_text": (
                    image.default_alt_text if image else ""
                ),  # THIS IS THE ONLY CHANGE
            }
            for image in image_values
        ]

    else:
        # Treat `values` as the standard ImageBlock representation - a (possibly empty) list of
        # dicts containing `image`, `decorative` and `alt_text` keys to be handled by the
        # StructBlock superclass
        struct_values = super(ImageBlock, self).bulk_to_python(values)

    return [self._struct_value_to_image(struct_value) for struct_value in struct_values]


# Import the module or class we're patching, then patch it with the above function(s).
ImageBlock.to_python = to_python_with_default_alt
ImageBlock.bulk_to_python = bulk_to_python_with_default_alt
