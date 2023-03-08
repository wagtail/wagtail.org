import django.db.models.deletion
from django.db import migrations, models

import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ("images", "__first__"),
        ("wagtailimages", "0006_add_verbose_names"),
        ("core", "0002_homepage_secondary_carousel_introduction"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageMainCarouselItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("tab_title", models.CharField(max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("summary", models.CharField(max_length=511)),
                ("video", models.URLField()),
                (
                    "call_to_action_url",
                    models.URLField(blank=True, verbose_name="Call to action URL"),
                ),
                (
                    "call_to_action_caption",
                    models.CharField(blank=True, max_length=255),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="images.WagtailIOImage",
                        null=True,
                        related_name="+",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        to="core.HomePage", related_name="main_carousel_items"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="HomePageSecondaryCarouselItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("title", models.CharField(max_length=255)),
                ("blockquote", models.CharField(max_length=511)),
                ("author_name", models.CharField(max_length=255)),
                ("author_job", models.CharField(max_length=255)),
                ("website", models.URLField(blank=True)),
                (
                    "author_image",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="wagtailimages.Image",
                        null=True,
                        related_name="+",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="images.WagtailIOImage",
                        null=True,
                        related_name="+",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        to="core.HomePage", related_name="secondary_carousel_items"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
    ]
