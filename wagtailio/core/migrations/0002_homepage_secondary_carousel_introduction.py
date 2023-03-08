from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="secondary_carousel_introduction",
            field=models.CharField(default="", max_length=511),
            preserve_default=False,
        ),
    ]
