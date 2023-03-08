from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0019_auto_20150527_1450"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsletterEmailAddress",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                ("email", models.EmailField(max_length=75)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
