# Generated by Django 3.2.16 on 2022-10-04 12:34

import wagtail.blocks
import wagtail.fields

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("features", "0012_alter_featureindexpage_features"),
    ]

    operations = [
        migrations.AlterField(
            model_name="featureindexpage",
            name="cta",
            field=wagtail.fields.StreamField(
                [
                    (
                        "cta",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "cta",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "text",
                                                wagtail.blocks.CharBlock(
                                                    label="CTA text",
                                                    max_length=255,
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "cta_page",
                                                wagtail.blocks.PageChooserBlock(
                                                    label="CTA page", required=False
                                                ),
                                            ),
                                            (
                                                "cta_url",
                                                wagtail.blocks.URLBlock(
                                                    label="CTA URL", required=False
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.TextBlock(
                                        label="Short description",
                                        max_length=100,
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="featureindexpage",
            name="features",
            field=wagtail.fields.StreamField(
                [
                    (
                        "features",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "blocks",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "heading",
                                                    wagtail.blocks.CharBlock(
                                                        max_length=255
                                                    ),
                                                ),
                                                (
                                                    "features",
                                                    wagtail.blocks.ListBlock(
                                                        wagtail.blocks.StructBlock(
                                                            [
                                                                (
                                                                    "heading",
                                                                    wagtail.blocks.CharBlock(
                                                                        label="Feature heading",
                                                                        max_length=255,
                                                                        required=False,
                                                                    ),
                                                                ),
                                                                (
                                                                    "description",
                                                                    wagtail.blocks.RichTextBlock(
                                                                        features=[
                                                                            "bold",
                                                                            "italic",
                                                                            "link",
                                                                            "document",
                                                                        ],
                                                                        label="Feature description",
                                                                        required=True,
                                                                    ),
                                                                ),
                                                                (
                                                                    "link",
                                                                    wagtail.blocks.URLBlock(
                                                                        label="Feature link",
                                                                        required=False,
                                                                    ),
                                                                ),
                                                                (
                                                                    "link_title",
                                                                    wagtail.blocks.CharBlock(
                                                                        default="View docs",
                                                                        label="Feature link title",
                                                                        max_length=50,
                                                                        required=False,
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                        min_num=2,
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]
