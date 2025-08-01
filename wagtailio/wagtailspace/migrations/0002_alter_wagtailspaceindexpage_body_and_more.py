# Generated by Django 5.1.6 on 2025-07-23 19:43

from django.db import migrations

import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailspace", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wagtailspaceindexpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", 1),
                    ("centered_text", 1),
                    ("image", 2),
                    ("cta_button", 6),
                    ("speaker_highlight", 13),
                    ("sponsor_highlight", 18),
                ],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "h2",
                                "h3",
                                "ol",
                                "ul",
                                "link",
                                "document",
                            ],
                            "required": True,
                        },
                    ),
                    1: ("wagtail.blocks.StructBlock", [[("rich_text", 0)]], {}),
                    2: ("wagtail.images.blocks.ImageBlock", [], {}),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "CTA text", "max_length": 255, "required": False},
                    ),
                    4: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {"label": "CTA page", "required": False},
                    ),
                    5: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "CTA URL", "required": False},
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 3), ("cta_page", 4), ("cta_url", 5)]],
                        {},
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 255, "required": False},
                    ),
                    8: (
                        "wagtail.images.blocks.ImageBlock",
                        [],
                        {"help_text": "Use a square image for best results."},
                    ),
                    9: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 255, "required": True},
                    ),
                    10: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {"max_length": 255, "required": False},
                    ),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("speaker_image", 8),
                                ("speaker_name", 9),
                                ("speaker_talk", 10),
                            ]
                        ],
                        {},
                    ),
                    12: (
                        "wagtail.blocks.StreamBlock",
                        [[("speaker", 11)]],
                        {"blank": True, "max_num": 4},
                    ),
                    13: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 7), ("speaker", 12)]],
                        {},
                    ),
                    14: ("wagtail.blocks.ListBlock", (2,), {}),
                    15: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "Sponsor Link", "required": False},
                    ),
                    16: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("sponsor_type", 9),
                                ("sponsor_logo", 14),
                                ("sponsor_link", 15),
                            ]
                        ],
                        {},
                    ),
                    17: (
                        "wagtail.blocks.StreamBlock",
                        [[("sponsor", 16)]],
                        {"blank": True},
                    ),
                    18: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 7), ("sponsor", 17)]],
                        {},
                    ),
                },
            ),
        ),
        migrations.AlterField(
            model_name="wagtailspacepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", 1),
                    ("centered_text", 1),
                    ("image", 2),
                    ("cta_button", 6),
                    ("speaker_highlight", 13),
                    ("sponsor_highlight", 18),
                ],
                blank=True,
                block_lookup={
                    0: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "features": [
                                "bold",
                                "italic",
                                "h2",
                                "h3",
                                "ol",
                                "ul",
                                "link",
                                "document",
                            ],
                            "required": True,
                        },
                    ),
                    1: ("wagtail.blocks.StructBlock", [[("rich_text", 0)]], {}),
                    2: ("wagtail.images.blocks.ImageBlock", [], {}),
                    3: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "CTA text", "max_length": 255, "required": False},
                    ),
                    4: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {"label": "CTA page", "required": False},
                    ),
                    5: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "CTA URL", "required": False},
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 3), ("cta_page", 4), ("cta_url", 5)]],
                        {},
                    ),
                    7: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 255, "required": False},
                    ),
                    8: (
                        "wagtail.images.blocks.ImageBlock",
                        [],
                        {"help_text": "Use a square image for best results."},
                    ),
                    9: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 255, "required": True},
                    ),
                    10: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {"max_length": 255, "required": False},
                    ),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("speaker_image", 8),
                                ("speaker_name", 9),
                                ("speaker_talk", 10),
                            ]
                        ],
                        {},
                    ),
                    12: (
                        "wagtail.blocks.StreamBlock",
                        [[("speaker", 11)]],
                        {"blank": True, "max_num": 4},
                    ),
                    13: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 7), ("speaker", 12)]],
                        {},
                    ),
                    14: ("wagtail.blocks.ListBlock", (2,), {}),
                    15: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "Sponsor Link", "required": False},
                    ),
                    16: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("sponsor_type", 9),
                                ("sponsor_logo", 14),
                                ("sponsor_link", 15),
                            ]
                        ],
                        {},
                    ),
                    17: (
                        "wagtail.blocks.StreamBlock",
                        [[("sponsor", 16)]],
                        {"blank": True},
                    ),
                    18: (
                        "wagtail.blocks.StructBlock",
                        [[("heading", 7), ("sponsor", 17)]],
                        {},
                    ),
                },
            ),
        ),
    ]
