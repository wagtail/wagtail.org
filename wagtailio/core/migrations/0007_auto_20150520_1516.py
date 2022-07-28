# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_featureaspect_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepagesecondarycarouselitem",
            name="author_image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.WagtailIOImage",
                blank=True,
                related_name="+",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
