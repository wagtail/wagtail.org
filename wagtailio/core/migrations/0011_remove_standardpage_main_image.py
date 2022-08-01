# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_auto_20150522_1504"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="standardpage",
            name="main_image",
        ),
    ]
