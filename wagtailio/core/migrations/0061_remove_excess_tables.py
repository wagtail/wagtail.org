# Generated by Django 5.1.5 on 2025-01-24 22:38

from django.db import migrations


class Migration(migrations.Migration):
    """
    The Wagtail AB Testing module as well as the Google import module were removed from this project without dropping its tables.
    """

    dependencies = [
        ("core", "0060_alter_contentpage_body_alter_homepage_body"),
    ]

    operations = [
        migrations.RunSQL(
            elidable=True,  # This migration can be removed during a squash
            sql=[
                "DROP TABLE IF EXISTS wagtail_ab_testing_abtesthourlylog;",
                "DROP TABLE IF EXISTS wagtail_ab_testing_abtest;",
                "DROP TABLE IF EXISTS wagtail_image_import_driveidmapping;",
            ],
            reverse_sql=[migrations.RunSQL.noop, migrations.RunSQL.noop],
        )
    ]
