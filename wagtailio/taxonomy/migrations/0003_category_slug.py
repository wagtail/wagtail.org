from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Category = apps.get_model("taxonomy", "Category")
    for category in Category.objects.all():
        category.slug = slugify(category.title)
        category.save(update_fields=["slug"])


class Migration(migrations.Migration):
    dependencies = [
        ("taxonomy", "0002_update_svg_icon_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=128, null=True, db_index=False),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=128, unique=True),
        ),
    ]
