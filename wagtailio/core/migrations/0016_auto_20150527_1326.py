# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '__first__'),
        ('core', '0015_auto_20150527_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurepage',
            name='listing_image',
            field=models.ForeignKey(help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', to='images.WagtailIOImage', related_name='+', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepage',
            name='listing_intro',
            field=models.TextField(help_text='Summary of this page to display when this is linked from elsewhere in the site.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepage',
            name='social_image',
            field=models.ForeignKey(help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", to='images.WagtailIOImage', related_name='+', blank=True, verbose_name='Meta image', null=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepage',
            name='social_text',
            field=models.CharField(max_length=255, help_text='Description of this page as it should appear when shared on social networks, or in Google results', verbose_name='Meta description', blank=True),
            preserve_default=True,
        ),
    ]
