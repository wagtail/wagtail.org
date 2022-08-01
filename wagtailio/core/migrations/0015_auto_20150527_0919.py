# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_featureindexpage_featureindexpagemenuoption"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepagesecondarycarouselitem",
            name="blockquote",
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
