# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20150430_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='listing_image',
            field=models.ForeignKey(related_name='+', blank=True, to='images.WagtailIOImage', on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='homepage',
            name='social_image',
            field=models.ForeignKey(to='images.WagtailIOImage', related_name='+', blank=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
    ]
