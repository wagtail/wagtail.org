# Generated by Django 1.9.8 on 2016-07-27 11:08

import wagtail.images.models

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0003_wagtailioimage_collection"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wagtailiorendition",
            name="file",
            field=models.ImageField(
                height_field="height",
                upload_to=wagtail.images.models.get_rendition_upload_to,
                width_field="width",
            ),
        ),
    ]
