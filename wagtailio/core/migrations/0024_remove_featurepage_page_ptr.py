# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_developerspage_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featurepage',
            name='page_ptr',
        ),
    ]
