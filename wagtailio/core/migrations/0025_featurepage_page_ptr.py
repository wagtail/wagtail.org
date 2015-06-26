# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('core', '0024_remove_featurepage_page_ptr'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurepage',
            name='page_ptr',
            field=models.OneToOneField(auto_created=True, primary_key=True, to='wagtailcore.Page', default='', serialize=False, parent_link=True),
            preserve_default=False,
        ),
    ]
