# Generated by Django 1.9 on 2016-01-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_auto_20160121_1419"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsletteremailaddress",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
