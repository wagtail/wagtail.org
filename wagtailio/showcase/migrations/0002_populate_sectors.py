from django.db import migrations

SECTOR_DATA = (
    "Government agencies",
    "Corporations",
    "Education",
    "Cultural institutions",
    "Charities and nonprofits",
)


def _populate_sector_data(apps, schema_editor):
    Sector = apps.get_model("showcase", "Sector")
    to_create = []
    for name in SECTOR_DATA:
        to_create.append(Sector(name=name))
    Sector.objects.bulk_create(to_create)


def _remove_sector_data(apps, schema_editor):
    Sector = apps.get_model("showcase", "Sector")
    Sector.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("showcase", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=_populate_sector_data,
            reverse_code=_remove_sector_data,
        ),
    ]
