# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '__first__'),
        ('core', '0012_developerspage_developerspageoptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagesecondarycarouselitem',
            name='image',
        ),
        migrations.AddField(
            model_name='homepagesecondarycarouselitem',
            name='desktop_image',
            field=models.ForeignKey(default=1, related_name='+', to='images.WagtailIOImage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepagesecondarycarouselitem',
            name='mobile_image',
            field=models.ForeignKey(default=1, related_name='+', to='images.WagtailIOImage'),
            preserve_default=False,
        ),
    ]
