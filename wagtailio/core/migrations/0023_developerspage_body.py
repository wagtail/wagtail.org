# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_remove_homepagemaincarouselitem_tab_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="developerspage",
            name="body",
            field=wagtail.core.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
