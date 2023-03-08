from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_auto_20150522_1504"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="standardpage",
            name="main_image",
        ),
    ]
