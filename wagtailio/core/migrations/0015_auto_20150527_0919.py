from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_featureindexpage_featureindexpagemenuoption"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepagesecondarycarouselitem",
            name="blockquote",
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
