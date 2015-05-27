# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_developerspage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developerspageoptions',
            name='icon',
            field=models.CharField(choices=[('fa-github', 'Github'), ('fa-google', 'Google'), ('fa-eye', 'Eye'), ('fa-server', 'Servers')], max_length=255),
            preserve_default=True,
        ),
    ]
