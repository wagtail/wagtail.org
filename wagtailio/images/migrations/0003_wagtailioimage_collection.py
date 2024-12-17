# Generated by Django 1.9.8 on 2016-07-27 09:51

import django.db.models.deletion
import wagtail.models

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0028_merge"),
        ("images", "0002_update_to_wagtail_13"),
    ]

    operations = [
        migrations.AddField(
            model_name="wagtailioimage",
            name="collection",
            field=models.ForeignKey(
                default=wagtail.models.get_root_collection_id,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="wagtailcore.Collection",
                verbose_name="collection",
            ),
        ),
    ]
