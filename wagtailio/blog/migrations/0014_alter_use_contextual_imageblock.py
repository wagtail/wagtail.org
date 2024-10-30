# Generated by Django 5.0.9 on 2024-10-30 21:12

from django.db import migrations

import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_alter_blogpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("h2", 0),
                    ("h3", 1),
                    ("h4", 2),
                    ("paragraph", 3),
                    ("blockquote", 4),
                    ("image", 5),
                    ("document", 6),
                    ("embed", 7),
                    ("markdown", 8),
                    ("codeblock", 11),
                    ("teaser", 17),
                    ("get_started_block", 18),
                    ("sign_up_form", 19),
                    ("highlight", 28),
                    ("standalone_cta", 30),
                ],
                block_lookup={
                    0: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "title",
                            "icon": "title",
                            "template": "patterns/components/streamfields/headings/heading-2.html",
                        },
                    ),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "title",
                            "icon": "title",
                            "template": "patterns/components/streamfields/headings/heading-3.html",
                        },
                    ),
                    2: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "title",
                            "icon": "title",
                            "template": "patterns/components/streamfields/headings/heading-4.html",
                        },
                    ),
                    3: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "icon": "pilcrow",
                            "template": "patterns/components/streamfields/rich_text_block/rich_text_block.html",
                        },
                    ),
                    4: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "form_classname": "title",
                            "icon": "openquote",
                            "template": "patterns/components/streamfields/quotes/standalone_quote_block.html",
                        },
                    ),
                    5: (
                        "wagtail.images.blocks.ImageBlock",
                        [],
                        {
                            "icon": "image",
                            "template": "patterns/components/streamfields/image/image.html",
                        },
                    ),
                    6: (
                        "wagtail.documents.blocks.DocumentChooserBlock",
                        (),
                        {
                            "icon": "doc-full-inverse",
                            "template": "patterns/components/streamfields/document/document.html",
                        },
                    ),
                    7: (
                        "wagtail.embeds.blocks.EmbedBlock",
                        (),
                        {
                            "icon": "code",
                            "template": "patterns/components/streamfields/embed/embed.html",
                        },
                    ),
                    8: (
                        "wagtailio.utils.blocks.MarkDownBlock",
                        (),
                        {
                            "template": "patterns/components/streamfields/code_block/code_block.html"
                        },
                    ),
                    9: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bash", "Bash/Shell"),
                                ("css", "CSS"),
                                ("django", "Django templating language"),
                                ("html", "HTML"),
                                ("javascript", "Javascript"),
                                ("python", "Python"),
                                ("scss", "SCSS"),
                            ]
                        },
                    ),
                    10: ("wagtail.blocks.TextBlock", (), {}),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [[("language", 9), ("code", 10)]],
                        {
                            "template": "patterns/components/streamfields/code_block/code_block.html"
                        },
                    ),
                    12: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {"page_type": ["blog.BlogPage"], "required": False},
                    ),
                    13: ("wagtail.blocks.URLBlock", (), {"required": False}),
                    14: ("wagtail.images.blocks.ImageBlock", [], {}),
                    15: ("wagtail.blocks.TextBlock", (), {"required": False}),
                    16: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {"label": "Subheading for external link", "required": False},
                    ),
                    17: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("page", 12),
                                ("url_chooser", 13),
                                ("image_for_external_link", 14),
                                ("heading_for_external_link", 15),
                                ("subheading_for_ext_link", 16),
                            ]
                        ],
                        {"group": "CTA options"},
                    ),
                    18: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("core.GetStartedSnippet",),
                        {
                            "group": "CTA options",
                            "icon": "table-list",
                            "template": "patterns/components/streamfields/get_started_block/get_started_block.html",
                        },
                    ),
                    19: (
                        "wagtail.snippets.blocks.SnippetChooserBlock",
                        ("core.SignupFormSnippet",),
                        {
                            "group": "CTA options",
                            "icon": "envelope-open-text",
                            "template": "patterns/components/streamfields/sign_up_form_block/sign_up_form_block.html",
                        },
                    ),
                    20: ("wagtail.blocks.CharBlock", (), {"max_length": 100}),
                    21: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {"default": False, "required": False},
                    ),
                    22: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 50, "required": False},
                    ),
                    23: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("arrow-alt", "Arrow alt"),
                                ("arrow-in-circle", "Arrow in circle"),
                                ("arrow-in-square", "Arrow in square"),
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
                                ("magnifying-glass", "Magnifying Glass"),
                                ("money", "Money"),
                                ("moon", "Moon"),
                                ("one-two-steps", "One Two Steps"),
                                ("padlock", "Padlock"),
                                ("paper-plane", "Paper Plane"),
                                ("paper-stack", "Paper Stack"),
                                ("pen-checkbox", "Pen Checkbox"),
                                ("person-in-tie", "Person in Tie"),
                                ("python", "Python"),
                                ("question-mark-circle", "Question Mark Circle"),
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
                            ],
                            "required": False,
                        },
                    ),
                    24: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "CTA text", "max_length": 255, "required": False},
                    ),
                    25: (
                        "wagtail.blocks.PageChooserBlock",
                        (),
                        {"label": "CTA page", "required": False},
                    ),
                    26: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {"label": "CTA URL", "required": False},
                    ),
                    27: (
                        "wagtail.blocks.StructBlock",
                        [[("text", 24), ("cta_page", 25), ("cta_url", 26)]],
                        {},
                    ),
                    28: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("heading", 20),
                                ("description", 15),
                                ("image", 14),
                                ("image_on_right", 21),
                                ("meta_text", 22),
                                ("meta_icon", 23),
                                ("cta", 27),
                            ]
                        ],
                        {},
                    ),
                    29: (
                        "wagtail.blocks.TextBlock",
                        (),
                        {
                            "label": "Short description",
                            "max_length": 100,
                            "required": False,
                        },
                    ),
                    30: (
                        "wagtail.blocks.StructBlock",
                        [[("cta", 27), ("description", 29)]],
                        {"group": "CTA options"},
                    ),
                },
            ),
        ),
    ]
