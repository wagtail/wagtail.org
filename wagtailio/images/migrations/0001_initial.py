# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models

import wagtail.images.models
import wagtail.search.index

import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0006_add_verbose_names"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("taggit", "0002_auto_20150616_2121"),
    ]

    operations = [
        migrations.CreateModel(
            name="WagtailIOImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                ("title", models.CharField(verbose_name="Title", max_length=255)),
                (
                    "file",
                    models.ImageField(
                        height_field="height",
                        verbose_name="File",
                        upload_to=wagtail.images.models.get_upload_to,
                        width_field="width",
                    ),
                ),
                ("width", models.IntegerField(verbose_name="Width", editable=False)),
                ("height", models.IntegerField(verbose_name="Height", editable=False)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                ("focal_point_x", models.PositiveIntegerField(blank=True, null=True)),
                ("focal_point_y", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "focal_point_width",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "focal_point_height",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "alternative_text",
                    models.CharField(
                        help_text="The alternative text for the image, provided for the benefit of visually impaired users",
                        blank=True,
                        max_length=255,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        verbose_name="Tags",
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        verbose_name="Uploaded by user",
                        blank=True,
                        null=True,
                        to=settings.AUTH_USER_MODEL,
                        editable=False,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="WagtailIORendition",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        upload_to="images", height_field="height", width_field="width"
                    ),
                ),
                ("width", models.IntegerField(editable=False)),
                ("height", models.IntegerField(editable=False)),
                (
                    "focal_point_key",
                    models.CharField(
                        blank=True, default="", max_length=255, editable=False
                    ),
                ),
                ("filter", models.IntegerField(blank=True, null=True)),
                (
                    "image",
                    models.ForeignKey(
                        to="images.WagtailIOImage",
                        related_name="renditions",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="wagtailiorendition",
            unique_together=set([("image", "filter", "focal_point_key")]),
        ),
    ]
