# Generated by Django 3.2.12 on 2022-08-30 18:51

import django.db.models.deletion
from django.db import migrations, models

import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0066_collection_management_permissions"),
        ("core", "0046_update_svg_icon_list"),
    ]

    operations = [
        migrations.CreateModel(
            name="FooterMenuSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "sections",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "section",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "heading",
                                            wagtail.core.blocks.CharBlock(
                                                max_length=255
                                            ),
                                        ),
                                        (
                                            "links",
                                            wagtail.core.blocks.ListBlock(
                                                wagtail.core.blocks.StructBlock(
                                                    [
                                                        (
                                                            "text",
                                                            wagtail.core.blocks.CharBlock(
                                                                max_length=100
                                                            ),
                                                        ),
                                                        (
                                                            "cta_page",
                                                            wagtail.core.blocks.PageChooserBlock(
                                                                label="Page",
                                                                required=False,
                                                            ),
                                                        ),
                                                        (
                                                            "cta_url",
                                                            wagtail.core.blocks.URLBlock(
                                                                label="URL",
                                                                required=False,
                                                            ),
                                                        ),
                                                    ]
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "Footer menu",
            },
        ),
        migrations.CreateModel(
            name="MainMenuItemSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "nav_items",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "nav_item",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            wagtail.core.blocks.CharBlock(
                                                label="Nav item name", max_length=55
                                            ),
                                        ),
                                        (
                                            "short_description",
                                            wagtail.core.blocks.CharBlock(
                                                max_length=55, required=False
                                            ),
                                        ),
                                        (
                                            "icon",
                                            wagtail.core.blocks.ChoiceBlock(
                                                choices=[
                                                    ("arrow-alt", "Arrow alt"),
                                                    (
                                                        "arrow-in-circle",
                                                        "Arrow in circle",
                                                    ),
                                                    (
                                                        "arrow-in-square",
                                                        "Arrow in square",
                                                    ),
                                                    ("arrows", "Arrows"),
                                                    ("blog", "Blog"),
                                                    ("bread", "Bread"),
                                                    ("briefcase", "Briefcase"),
                                                    ("building", "Building"),
                                                    ("calendar", "Calendar"),
                                                    ("code-file", "Code File"),
                                                    ("document", "Document"),
                                                    ("envelope", "Envelope"),
                                                    ("explanation", "Explanation"),
                                                    ("eye", "Eye"),
                                                    ("flame", "Flame"),
                                                    ("friends", "Friends"),
                                                    ("github", "Github"),
                                                    ("handshake", "Handshake"),
                                                    ("heart", "Heart"),
                                                    ("history", "History"),
                                                    ("id-card", "ID Card"),
                                                    ("image", "Image"),
                                                    ("knife-fork", "Knife Fork"),
                                                    ("leaf", "Leaf"),
                                                    ("location-pin", "Location Pin"),
                                                    ("map", "Map"),
                                                    (
                                                        "magnifying-glass",
                                                        "Magnifying Glass",
                                                    ),
                                                    ("money", "Money"),
                                                    ("moon", "Moon"),
                                                    ("one-two-steps", "One Two Steps"),
                                                    ("padlock", "Padlock"),
                                                    ("paper-plane", "Paper Plane"),
                                                    ("paper-stack", "Paper Stack"),
                                                    ("pen-checkbox", "Pen Checkbox"),
                                                    ("person-in-tie", "Person in Tie"),
                                                    ("python", "Python"),
                                                    (
                                                        "question-mark-circle",
                                                        "Question Mark Circle",
                                                    ),
                                                    ("quotes", "Quotes"),
                                                    ("release-cycle", "Release Cycle"),
                                                    ("roadmap", "Roadmap"),
                                                    ("rocket", "Rocket"),
                                                    ("rollback", "Rollback"),
                                                    ("slack", "Slack"),
                                                    ("speech-bubble", "Speech Bubble"),
                                                    ("sun-cloud", "Sun Cloud"),
                                                    ("table-tennis", "Table Tennis"),
                                                    ("tree", "Tree"),
                                                    ("wordpress", "Wordpress"),
                                                    ("world", "World"),
                                                ]
                                            ),
                                        ),
                                        (
                                            "cta_page",
                                            wagtail.core.blocks.PageChooserBlock(
                                                label="Page", required=False
                                            ),
                                        ),
                                        (
                                            "cta_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="External Link", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
                (
                    "call_to_action",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "cta",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "text",
                                            wagtail.core.blocks.CharBlock(
                                                label="Heading", max_length=255
                                            ),
                                        ),
                                        (
                                            "sub_heading",
                                            wagtail.core.blocks.CharBlock(
                                                max_length=255, required=False
                                            ),
                                        ),
                                        (
                                            "description",
                                            wagtail.core.blocks.CharBlock(
                                                max_length=255, required=False
                                            ),
                                        ),
                                        (
                                            "icon",
                                            wagtail.core.blocks.ChoiceBlock(
                                                choices=[
                                                    ("arrow-alt", "Arrow alt"),
                                                    (
                                                        "arrow-in-circle",
                                                        "Arrow in circle",
                                                    ),
                                                    (
                                                        "arrow-in-square",
                                                        "Arrow in square",
                                                    ),
                                                    ("arrows", "Arrows"),
                                                    ("blog", "Blog"),
                                                    ("bread", "Bread"),
                                                    ("briefcase", "Briefcase"),
                                                    ("building", "Building"),
                                                    ("calendar", "Calendar"),
                                                    ("code-file", "Code File"),
                                                    ("document", "Document"),
                                                    ("envelope", "Envelope"),
                                                    ("explanation", "Explanation"),
                                                    ("eye", "Eye"),
                                                    ("flame", "Flame"),
                                                    ("friends", "Friends"),
                                                    ("github", "Github"),
                                                    ("handshake", "Handshake"),
                                                    ("heart", "Heart"),
                                                    ("history", "History"),
                                                    ("id-card", "ID Card"),
                                                    ("image", "Image"),
                                                    ("knife-fork", "Knife Fork"),
                                                    ("leaf", "Leaf"),
                                                    ("location-pin", "Location Pin"),
                                                    ("map", "Map"),
                                                    (
                                                        "magnifying-glass",
                                                        "Magnifying Glass",
                                                    ),
                                                    ("money", "Money"),
                                                    ("moon", "Moon"),
                                                    ("one-two-steps", "One Two Steps"),
                                                    ("padlock", "Padlock"),
                                                    ("paper-plane", "Paper Plane"),
                                                    ("paper-stack", "Paper Stack"),
                                                    ("pen-checkbox", "Pen Checkbox"),
                                                    ("person-in-tie", "Person in Tie"),
                                                    ("python", "Python"),
                                                    (
                                                        "question-mark-circle",
                                                        "Question Mark Circle",
                                                    ),
                                                    ("quotes", "Quotes"),
                                                    ("release-cycle", "Release Cycle"),
                                                    ("roadmap", "Roadmap"),
                                                    ("rocket", "Rocket"),
                                                    ("rollback", "Rollback"),
                                                    ("slack", "Slack"),
                                                    ("speech-bubble", "Speech Bubble"),
                                                    ("sun-cloud", "Sun Cloud"),
                                                    ("table-tennis", "Table Tennis"),
                                                    ("tree", "Tree"),
                                                    ("wordpress", "Wordpress"),
                                                    ("world", "World"),
                                                ]
                                            ),
                                        ),
                                        (
                                            "cta_page",
                                            wagtail.core.blocks.PageChooserBlock(
                                                label="Page", required=False
                                            ),
                                        ),
                                        (
                                            "cta_url",
                                            wagtail.core.blocks.URLBlock(
                                                label="External Link", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            )
                        ],
                        blank=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Main menu item",
            },
        ),
        migrations.CreateModel(
            name="MainMenuSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Main menu",
            },
        ),
        migrations.CreateModel(
            name="NavigationSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "footer_navigation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="navigation.footermenusnippet",
                    ),
                ),
                (
                    "get_started_menu",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="core.getstartedsnippet",
                    ),
                ),
                (
                    "main_navigation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="navigation.mainmenusnippet",
                    ),
                ),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MainMenuItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "menu_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="navigation.mainmenuitemsnippet",
                    ),
                ),
                (
                    "parent",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="navigation.mainmenusnippet",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
