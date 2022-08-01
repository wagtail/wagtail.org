# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_auto_20150527_1347"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="developerspage",
            name="body",
        ),
    ]
