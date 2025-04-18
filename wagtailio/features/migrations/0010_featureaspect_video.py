# Generated by Django 2.2.24 on 2021-07-16 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailmedia", "0004_duration_optional_floatfield"),
        ("features", "0009_featuredescription_airtable_record_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="featureaspect",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailmedia.Media",
            ),
        ),
    ]
