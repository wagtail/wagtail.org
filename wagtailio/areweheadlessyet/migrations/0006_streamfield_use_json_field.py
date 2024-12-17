# Generated by Django 3.2.16 on 2022-10-04 12:34

import wagtail.blocks
import wagtail.fields

from django.db import migrations

import wagtailio.areweheadlessyet.blocks


class Migration(migrations.Migration):
    dependencies = [
        (
            "areweheadlessyet",
            "0005_change_rich_text_api_representation0005_change_rich_text_api_representation",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="areweheadlessyethomepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                (
                                    "content",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "text",
                                                wagtailio.areweheadlessyet.blocks.RichTextBlockWithExpandedApiRepresentation(),
                                            ),
                                            (
                                                "link_group",
                                                wagtail.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "link",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    (
                                                                        "link",
                                                                        wagtail.blocks.URLBlock(
                                                                            required=True
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "link_text",
                                                                        wagtail.blocks.CharBlock(
                                                                            required=True
                                                                        ),
                                                                    ),
                                                                ]
                                                            ),
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "news",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                (
                                    "blog_posts",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "blog_post",
                                                wagtailio.areweheadlessyet.blocks.BlogPostChooserBlock(
                                                    page_type=["blog.BlogPage"]
                                                ),
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "topics",
                        wagtail.blocks.StructBlock(
                            [("title", wagtail.blocks.CharBlock())]
                        ),
                    ),
                    (
                        "issues",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                ("summary", wagtail.blocks.CharBlock(required=False)),
                                (
                                    "issues",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "issue",
                                                wagtailio.areweheadlessyet.blocks.IssueChooserBlock(
                                                    "areweheadlessyet.WagtailHeadlessIssue"
                                                ),
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
        migrations.AlterField(
            model_name="areweheadlessyettopicpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "text",
                        wagtailio.areweheadlessyet.blocks.RichTextBlockWithExpandedApiRepresentation(),
                    ),
                    (
                        "section",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                (
                                    "content",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "text",
                                                wagtailio.areweheadlessyet.blocks.RichTextBlockWithExpandedApiRepresentation(),
                                            ),
                                            (
                                                "link_group",
                                                wagtail.blocks.StreamBlock(
                                                    [
                                                        (
                                                            "link",
                                                            wagtail.blocks.StructBlock(
                                                                [
                                                                    (
                                                                        "link",
                                                                        wagtail.blocks.URLBlock(
                                                                            required=True
                                                                        ),
                                                                    ),
                                                                    (
                                                                        "link_text",
                                                                        wagtail.blocks.CharBlock(
                                                                            required=True
                                                                        ),
                                                                    ),
                                                                ]
                                                            ),
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "news",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock()),
                                (
                                    "blog_posts",
                                    wagtail.blocks.StreamBlock(
                                        [
                                            (
                                                "blog_post",
                                                wagtailio.areweheadlessyet.blocks.BlogPostChooserBlock(
                                                    page_type=["blog.BlogPage"]
                                                ),
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                use_json_field=True,
            ),
        ),
    ]
