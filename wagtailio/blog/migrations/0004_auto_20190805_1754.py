# Generated by Django 2.0.13 on 2019-08-05 17:54

from django.db import migrations

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks

import wagtailio.utils.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_blogpage_canonical_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "h2",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h3",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    (
                        "h4",
                        wagtail.core.blocks.CharBlock(classname="title", icon="title"),
                    ),
                    ("intro", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="pilcrow")),
                    (
                        "blockquote",
                        wagtail.core.blocks.CharBlock(
                            classname="title", icon="openquote"
                        ),
                    ),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    (
                        "document",
                        wagtail.documents.blocks.DocumentChooserBlock(
                            icon="doc-full-inverse"
                        ),
                    ),
                    (
                        "imagecaption",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                ("caption", wagtail.core.blocks.RichTextBlock()),
                            ],
                            label="Image caption",
                        ),
                    ),
                    (
                        "textimage",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("text", wagtail.core.blocks.RichTextBlock()),
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                                (
                                    "alignment",
                                    wagtailio.utils.blocks.SimpleImageFormatChoiceBlock(),
                                ),
                            ],
                            icon="image",
                        ),
                    ),
                    (
                        "colourtext",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("text", wagtail.core.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ],
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "calltoaction",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("text", wagtail.core.blocks.RichTextBlock()),
                                (
                                    "background",
                                    wagtailio.utils.blocks.BackgroundColourChoiceBlock(),
                                ),
                            ],
                            icon="pilcrow",
                        ),
                    ),
                    (
                        "tripleimage",
                        wagtail.core.blocks.StructBlock(
                            [
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
                            ],
                            icon="image",
                        ),
                    ),
                    (
                        "stats",
                        wagtail.core.blocks.ListBlock(
                            wagtail.core.blocks.StructBlock(
                                [
                                    (
                                        "image",
                                        wagtail.images.blocks.ImageChooserBlock(),
                                    ),
                                    ("stat", wagtail.core.blocks.CharBlock()),
                                    ("text", wagtail.core.blocks.CharBlock()),
                                ],
                                icon="code",
                            )
                        ),
                    ),
                    ("embed", wagtail.embeds.blocks.EmbedBlock(icon="code")),
                    ("markdown", wagtailio.utils.blocks.MarkDownBlock()),
                    (
                        "codeblock",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "language",
                                    wagtail.core.blocks.ChoiceBlock(
                                        choices=[
                                            ("bash", "Bash/Shell"),
                                            ("css", "CSS"),
                                            ("django", "Django templating language"),
                                            ("html", "HTML"),
                                            ("javascript", "Javascript"),
                                            ("python", "Python"),
                                            ("scss", "SCSS"),
                                        ]
                                    ),
                                ),
                                ("code", wagtail.core.blocks.TextBlock()),
                            ]
                        ),
                    ),
                    (
                        "backers",
                        wagtail.core.blocks.StructBlock(
                            [
                                (
                                    "gold_backers",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "name",
                                                    wagtail.core.blocks.CharBlock(),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "url",
                                                    wagtail.core.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "silver_backers",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "name",
                                                    wagtail.core.blocks.CharBlock(),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "url",
                                                    wagtail.core.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "bronze_backers",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "name",
                                                    wagtail.core.blocks.CharBlock(),
                                                ),
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "url",
                                                    wagtail.core.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "linked_backers",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [
                                                (
                                                    "name",
                                                    wagtail.core.blocks.CharBlock(),
                                                ),
                                                (
                                                    "url",
                                                    wagtail.core.blocks.URLBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "named_backers",
                                    wagtail.core.blocks.ListBlock(
                                        wagtail.core.blocks.StructBlock(
                                            [("name", wagtail.core.blocks.CharBlock())]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                ]
            ),
        ),
    ]
