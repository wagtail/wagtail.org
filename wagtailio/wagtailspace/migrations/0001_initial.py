# Generated by Django 5.1.6 on 2025-07-16 22:30

from django.db import migrations, models
import django.db.models.deletion

import wagtail.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("images", "0017_drop_obsolete_alternative_text"),
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpaceMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "menu_sections",
                    wagtail.fields.StreamField(
                        [("menu_section", 3)],
                        block_lookup={
                            0: ("wagtail.blocks.CharBlock", (), {"max_length": 255}),
                            1: (
                                "wagtail.blocks.PageChooserBlock",
                                (),
                                {"label": "Page", "required": False},
                            ),
                            2: (
                                "wagtail.blocks.URLBlock",
                                (),
                                {"label": "External Link", "required": False},
                            ),
                            3: (
                                "wagtail.blocks.StructBlock",
                                [
                                    [
                                        ("name", 0),
                                        ("space_menu_page", 1),
                                        ("space_menu_url", 2),
                                    ]
                                ],
                                {},
                            ),
                        },
                    ),
                ),
                ("registration_url", models.URLField(blank=True, default="")),
            ],
            options={
                "verbose_name": "Wagtail Space menu",
            },
        ),
        migrations.CreateModel(
            name="SpaceSocialSnippet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("heading", models.CharField(max_length=255)),
                ("subheading", wagtail.fields.RichTextField(max_length=255)),
                (
                    "social",
                    wagtail.fields.StreamField(
                        [("social", 3)],
                        block_lookup={
                            0: ("wagtail.blocks.CharBlock", (), {}),
                            1: ("wagtail.blocks.URLBlock", (), {}),
                            2: (
                                "wagtail.images.blocks.ImageBlock",
                                [],
                                {
                                    "help_text": "Max image width of 100px for best results."
                                },
                            ),
                            3: (
                                "wagtail.blocks.StructBlock",
                                [[("name", 0), ("url", 1), ("logo", 2)]],
                                {},
                            ),
                        },
                    ),
                ),
            ],
            options={
                "verbose_name": "Wagtail Space Social Menu",
            },
        ),
        migrations.CreateModel(
            name="WagtailSpaceIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "social_text",
                    models.CharField(
                        blank=True,
                        help_text="Description of this page as it should appear when shared on social networks, or in Google results",
                        max_length=255,
                        verbose_name="Meta description",
                    ),
                ),
                (
                    "listing_intro",
                    models.TextField(
                        blank=True,
                        help_text="Summary of this page to display when this is linked from elsewhere in the site.",
                    ),
                ),
                ("heading", models.TextField(blank=True, verbose_name="Heading")),
                (
                    "event_date_subhead",
                    models.TextField(blank=True, verbose_name="Event date"),
                ),
                ("tagline", models.TextField(blank=True, verbose_name="Tagline")),
                (
                    "cta",
                    wagtail.fields.StreamField(
                        [("cta", 3)],
                        blank=True,
                        block_lookup={
                            0: (
                                "wagtail.blocks.CharBlock",
                                (),
                                {
                                    "label": "CTA text",
                                    "max_length": 255,
                                    "required": False,
                                },
                            ),
                            1: (
                                "wagtail.blocks.PageChooserBlock",
                                (),
                                {"label": "CTA page", "required": False},
                            ),
                            2: (
                                "wagtail.blocks.URLBlock",
                                (),
                                {"label": "CTA URL", "required": False},
                            ),
                            3: (
                                "wagtail.blocks.StructBlock",
                                [[("text", 0), ("cta_page", 1), ("cta_url", 2)]],
                                {},
                            ),
                        },
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("rich_text", 1),
                            ("centered_text", 1),
                            ("image", 2),
                            ("cta_button", 6),
                            ("speaker_highlight", 13),
                            ("sponsor_highlight", 17),
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
                                {
                                    "label": "CTA text",
                                    "max_length": 255,
                                    "required": False,
                                },
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
                                "wagtail.blocks.StructBlock",
                                [[("sponsor_type", 9), ("sponsor_logo", 14)]],
                                {},
                            ),
                            16: (
                                "wagtail.blocks.StreamBlock",
                                [[("sponsor", 15)]],
                                {"blank": True},
                            ),
                            17: (
                                "wagtail.blocks.StructBlock",
                                [[("heading", 7), ("sponsor", 16)]],
                                {},
                            ),
                        },
                    ),
                ),
                (
                    "listing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image to display along with summary, when this page is linked from elsewhere in the site.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.wagtailioimage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image to appear alongside 'Meta description', particularly for sharing on social networks",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.wagtailioimage",
                        verbose_name="Meta image",
                    ),
                ),
                (
                    "space_social",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailspace.spacesocialsnippet",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="WagtailSpacePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "social_text",
                    models.CharField(
                        blank=True,
                        help_text="Description of this page as it should appear when shared on social networks, or in Google results",
                        max_length=255,
                        verbose_name="Meta description",
                    ),
                ),
                (
                    "listing_intro",
                    models.TextField(
                        blank=True,
                        help_text="Summary of this page to display when this is linked from elsewhere in the site.",
                    ),
                ),
                ("heading", models.TextField(blank=True, verbose_name="Heading")),
                (
                    "sub_heading",
                    models.TextField(blank=True, verbose_name="Sub heading"),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("rich_text", 1),
                            ("centered_text", 1),
                            ("image", 2),
                            ("cta_button", 6),
                            ("speaker_highlight", 13),
                            ("sponsor_highlight", 17),
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
                                {
                                    "label": "CTA text",
                                    "max_length": 255,
                                    "required": False,
                                },
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
                                "wagtail.blocks.StructBlock",
                                [[("sponsor_type", 9), ("sponsor_logo", 14)]],
                                {},
                            ),
                            16: (
                                "wagtail.blocks.StreamBlock",
                                [[("sponsor", 15)]],
                                {"blank": True},
                            ),
                            17: (
                                "wagtail.blocks.StructBlock",
                                [[("heading", 7), ("sponsor", 16)]],
                                {},
                            ),
                        },
                    ),
                ),
                (
                    "listing_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image to display along with summary, when this page is linked from elsewhere in the site.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.wagtailioimage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image to appear alongside 'Meta description', particularly for sharing on social networks",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.wagtailioimage",
                        verbose_name="Meta image",
                    ),
                ),
                (
                    "space_social",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailspace.spacesocialsnippet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Wagtail Space Page",
            },
            bases=("wagtailcore.page", models.Model),
        ),
    ]
