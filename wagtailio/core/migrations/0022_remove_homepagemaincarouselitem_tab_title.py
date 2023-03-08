from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0021_auto_20150528_1008"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="homepagemaincarouselitem",
            name="tab_title",
        ),
    ]
