# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '__first__'),
        ('core', '0007_auto_20150520_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255, blank=True)),
                ('url', models.URLField(blank=True)),
                ('image', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to='images.WagtailIOImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', null=True, to='core.Author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='introduction',
            field=models.CharField(max_length=511, default=''),
            preserve_default=False,
        ),
    ]
