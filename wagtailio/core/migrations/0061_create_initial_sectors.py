from django.db import migrations

SECTOR_DATA = (
    "Government agencies",
    "Corporations",
    "Education",
    "Cultural institutions",
    "Charities and nonprofits",
)


def _populate_sector_data(apps, schema_editor):
    Sector = apps.get_model("core", "Sector")
    to_create = []
    for name in SECTOR_DATA:
        to_create.append(Sector(name=name))
    Sector.objects.bulk_create(to_create)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0060_sector_showcaseitem_showcasepage"),
    ]

    operations = [
        migrations.RunPython(
            code=_populate_sector_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
