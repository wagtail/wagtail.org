from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_featureaspect_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepagesecondarycarouselitem",
            name="author_image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.WagtailIOImage",
                blank=True,
                related_name="+",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
