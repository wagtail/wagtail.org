# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 12:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("features", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bullet",
            options={"ordering": ["sort_order"]},
        ),
        migrations.AlterModelOptions(
            name="featurepagefeatureaspect",
            options={"ordering": ["sort_order"]},
        ),
        migrations.AlterModelTable(
            name="bullet",
            table=None,
        ),
        migrations.AlterModelTable(
            name="featureaspect",
            table=None,
        ),
        migrations.AlterModelTable(
            name="featureindexpage",
            table=None,
        ),
        migrations.AlterModelTable(
            name="featureindexpagemenuoption",
            table=None,
        ),
        migrations.AlterModelTable(
            name="featurepage",
            table=None,
        ),
        migrations.AlterModelTable(
            name="featurepagefeatureaspect",
            table=None,
        ),
    ]
