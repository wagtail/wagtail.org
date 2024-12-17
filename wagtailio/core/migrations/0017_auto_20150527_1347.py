import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_auto_20150527_1326"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepagesecondarycarouselitem",
            name="mobile_image",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.WagtailIOImage",
                related_name="+",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
