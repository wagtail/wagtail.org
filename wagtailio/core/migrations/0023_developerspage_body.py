from django.db import migrations, models

import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_remove_homepagemaincarouselitem_tab_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="developerspage",
            name="body",
            field=wagtail.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
