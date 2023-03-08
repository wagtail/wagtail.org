from django.db import migrations, models

import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0015_add_more_verbose_names"),
        ("core", "0004_auto_20150519_2040"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bullet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, null=True, editable=False),
                ),
                ("title", models.CharField(max_length=255)),
                ("text", wagtail.fields.RichTextField()),
                (
                    "snippet",
                    modelcluster.fields.ParentalKey(
                        related_name="bullets", to="core.FeatureAspect"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="FeaturePageFeatureAspect",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, null=True, editable=False),
                ),
                (
                    "feature_aspect",
                    models.ForeignKey(
                        related_name="+",
                        to="core.FeaturePage",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        related_name="feature_aspects", to="core.FeaturePage"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name="featureaspectbullet",
            name="model",
        ),
        migrations.DeleteModel(
            name="FeatureAspectBullet",
        ),
        migrations.AlterModelOptions(
            name="featureaspect",
            options={},
        ),
        migrations.RenameField(
            model_name="homepagemaincarouselitem",
            old_name="call_to_action_url",
            new_name="call_to_action_external_link",
        ),
        migrations.RemoveField(
            model_name="featureaspect",
            name="page",
        ),
        migrations.RemoveField(
            model_name="featureaspect",
            name="sort_order",
        ),
        migrations.AddField(
            model_name="homepagemaincarouselitem",
            name="call_to_action_internal_link",
            field=models.ForeignKey(
                blank=True,
                related_name="+",
                null=True,
                to="wagtailcore.Page",
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
    ]
