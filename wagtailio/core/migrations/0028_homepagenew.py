# Generated by Django 1.9 on 2016-04-14 11:22

from django.db import migrations, models
import django.db.models.deletion

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks

import wagtailio.utils.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0023_alter_page_revision_on_delete_behaviour"),
        ("images", "0002_update_to_wagtail_13"),
        ("core", "0027_update_to_wagtail_13"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageNew",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
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
                ("introduction", models.CharField(max_length=511)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        (
                            (
                                "h2",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h3",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "h4",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="title"
                                ),
                            ),
                            (
                                "intro",
                                wagtail.blocks.RichTextBlock(icon="pilcrow"),
                            ),
                            (
                                "paragraph",
                                wagtail.blocks.RichTextBlock(icon="pilcrow"),
                            ),
                            (
                                "blockquote",
                                wagtail.blocks.CharBlock(
                                    classname="title", icon="openquote"
                                ),
                            ),
                            (
                                "image",
                                wagtail.images.blocks.ImageChooserBlock(icon="image"),
                            ),
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
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.RichTextBlock(),
                                        ),
                                    ),
                                    label="Image caption",
                                ),
                            ),
                            (
                                "textimage",
                                wagtail.blocks.StructBlock(
                                    (
                                        ("text", wagtail.blocks.RichTextBlock()),
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
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
                            ("markdown", wagtailio.utils.blocks.MarkDownBlock()),
                            (
                                "codeblock",
                                wagtail.blocks.StructBlock(
                                    (
                                        (
                                            "language",
                                            wagtail.blocks.ChoiceBlock(
                                                choices=[
                                                    ("bash", "Bash/Shell"),
                                                    ("css", "CSS"),
                                                    (
                                                        "django",
                                                        "Django templating language",
                                                    ),
                                                    ("html", "HTML"),
                                                    ("javascript", "Javascript"),
                                                    ("python", "Python"),
                                                    ("scss", "SCSS"),
                                                ]
                                            ),
                                        ),
                                        ("code", wagtail.blocks.TextBlock()),
                                    )
                                ),
                            ),
                        )
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
                        to="images.WagtailIOImage",
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="images.WagtailIOImage",
                        verbose_name="Meta image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
    ]
