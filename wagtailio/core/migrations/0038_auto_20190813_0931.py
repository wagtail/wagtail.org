# Generated by Django 2.0.13 on 2019-08-13 09:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0037_auto_20180604_1629"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="social_image",
            field=models.ForeignKey(
                blank=True,
                help_text="Image to appear alongside 'Meta description', particularly for sharing on social networks",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="images.WagtailIOImage",
                verbose_name="Meta image",
            ),
        ),
    ]
