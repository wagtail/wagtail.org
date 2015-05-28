# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20150528_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagemaincarouselitem',
            name='tab_title',
        ),
    ]
