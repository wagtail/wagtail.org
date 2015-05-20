# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150520_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureaspect',
            name='title',
            field=models.CharField(max_length=255, default='test'),
            preserve_default=False,
        ),
    ]
