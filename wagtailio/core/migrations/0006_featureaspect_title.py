from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_auto_20150520_1429"),
    ]

    operations = [
        migrations.AddField(
            model_name="featureaspect",
            name="title",
            field=models.CharField(max_length=255, default="test"),
            preserve_default=False,
        ),
    ]
