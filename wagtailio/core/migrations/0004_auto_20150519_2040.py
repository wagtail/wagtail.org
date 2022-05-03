# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('images', '__first__'),
        ('core', '0003_homepagemaincarouselitem_homepagesecondarycarouselitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureAspect',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeatureAspectBullet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sort_order', models.IntegerField(editable=False, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('text', wagtail.fields.RichTextField()),
                ('model', modelcluster.fields.ParentalKey(related_name='bullets', to='core.FeatureAspect')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, to='wagtailcore.Page', serialize=False, on_delete=models.CASCADE)),
                ('introduction', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='featureaspect',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='feature_aspects', to='core.FeaturePage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featureaspect',
            name='screenshot',
            field=models.ForeignKey(related_name='+', to='images.WagtailIOImage', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
    ]
