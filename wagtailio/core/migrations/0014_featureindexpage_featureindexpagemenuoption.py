from django.db import migrations, models

import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0015_add_more_verbose_names"),
        ("core", "0013_auto_20150522_1639"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeatureIndexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        serialize=False,
                        parent_link=True,
                        primary_key=True,
                        to="wagtailcore.Page",
                        auto_created=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("introduction", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="FeatureIndexPageMenuOption",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("label", models.CharField(max_length=255)),
                (
                    "link",
                    models.ForeignKey(
                        to="wagtailcore.Page",
                        on_delete=models.CASCADE,
                        related_name="+",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        to="core.FeatureIndexPage",
                        related_name="secondary_menu_options",
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
