from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "__first__"),
        ("core", "0012_developerspage_developerspageoptions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="homepagesecondarycarouselitem",
            name="image",
        ),
        migrations.AddField(
            model_name="homepagesecondarycarouselitem",
            name="desktop_image",
            field=models.ForeignKey(
                default=1,
                related_name="+",
                to="images.WagtailIOImage",
                on_delete=models.CASCADE,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="homepagesecondarycarouselitem",
            name="mobile_image",
            field=models.ForeignKey(
                default=1,
                related_name="+",
                to="images.WagtailIOImage",
                on_delete=models.CASCADE,
            ),
            preserve_default=False,
        ),
    ]
