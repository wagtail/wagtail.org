# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='listing_image',
            field=models.ForeignKey(to='wagtailimages.Image', blank=True, null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='listing_intro',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='social_image',
            field=models.ForeignKey(to='wagtailimages.Image', blank=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", null=True, related_name='+', on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='social_text',
            field=models.CharField(blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results', max_length=255),
            preserve_default=True,
        ),
    ]
