from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0017_auto_20150527_1347"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="developerspage",
            name="body",
        ),
    ]
