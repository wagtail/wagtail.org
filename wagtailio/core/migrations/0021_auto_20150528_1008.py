# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks

import wagtailio.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_newsletteremailaddress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    (
                        "document",
                        wagtail.documents.blocks.DocumentChooserBlock(
                            icon="doc-full-inverse"
                        ),
                    ),
                    (
                        "imagecaption",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("caption", wagtail.blocks.RichTextBlock()),
                            ),
                            label="Image caption",
                        ),
                    ),
                    (
                        "textimage",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                                (
                                    "alignment",
                                    wagtailio.utils.blocks.SimpleImageFormatChoiceBlock(),
                                ),
                            ),
                            icon="image",
                        ),
                    ),
                    (
                        "colourtext",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ),
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "calltoaction",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ),
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "tripleimage",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "first_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                                (
                                    "second_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                                (
                                    "third_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                            ),
                            icon="image",
                        ),
                    ),
                    (
                        "stats",
                        wagtail.blocks.ListBlock(
                            wagtail.blocks.StructBlock(
                                (
                                    (
                                        "image",
                                        wagtail.images.blocks.ImageChooserBlock(),
                                    ),
                                    ("stat", wagtail.blocks.CharBlock()),
                                    ("text", wagtail.blocks.CharBlock()),
                                ),
                                icon="code",
                            )
                        ),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="standardpage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    (
                        "h2",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    (
                        "h3",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    (
                        "h4",
                        wagtail.blocks.CharBlock(icon="title", classname="title"),
                    ),
                    ("intro", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="pilcrow")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    (
                        "document",
                        wagtail.documents.blocks.DocumentChooserBlock(
                            icon="doc-full-inverse"
                        ),
                    ),
                    (
                        "imagecaption",
                        wagtail.blocks.StructBlock(
                            (
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("caption", wagtail.blocks.RichTextBlock()),
                            ),
                            label="Image caption",
                        ),
                    ),
                    (
                        "textimage",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                                (
                                    "alignment",
                                    wagtailio.utils.blocks.SimpleImageFormatChoiceBlock(),
                                ),
                            ),
                            icon="image",
                        ),
                    ),
                    (
                        "colourtext",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ),
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "calltoaction",
                        wagtail.blocks.StructBlock(
                            (
                                ("text", wagtail.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ),
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "tripleimage",
                        wagtail.blocks.StructBlock(
                            (
                                (
                                    "first_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                                (
                                    "second_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                                (
                                    "third_image",
                                    wagtail.images.blocks.ImageChooserBlock(),
                                ),
                            ),
                            icon="image",
                        ),
                    ),
                    (
                        "stats",
                        wagtail.blocks.ListBlock(
                            wagtail.blocks.StructBlock(
                                (
                                    (
                                        "image",
                                        wagtail.images.blocks.ImageChooserBlock(),
                                    ),
                                    ("stat", wagtail.blocks.CharBlock()),
                                    ("text", wagtail.blocks.CharBlock()),
                                ),
                                icon="code",
                            )
                        ),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
    ]
