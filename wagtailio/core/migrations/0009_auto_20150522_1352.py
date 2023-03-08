from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_auto_20150520_1554"),
    ]

    operations = [
        migrations.AlterField(
            model_name="featurepagefeatureaspect",
            name="feature_aspect",
            field=models.ForeignKey(
                to="core.FeatureAspect", related_name="+", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
    ]
