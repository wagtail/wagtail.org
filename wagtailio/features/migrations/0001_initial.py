# Generated by Django 1.9.8 on 2016-07-29 11:52

from django.db import migrations, models
import django.db.models.deletion

import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0028_merge"),
        ("images", "0004_auto_20160727_1108"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="Bullet",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "sort_order",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        ("title", models.CharField(max_length=255)),
                        ("text", wagtail.fields.RichTextField()),
                    ],
                    options={
                        "db_table": "core_bullet",
                    },
                ),
                migrations.CreateModel(
                    name="FeatureAspect",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("title", models.CharField(max_length=255)),
                        (
                            "screenshot",
                            models.ForeignKey(
                                blank=True,
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="+",
                                to="images.WagtailIOImage",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "core_featureaspect",
                    },
                ),
                migrations.CreateModel(
                    name="FeatureIndexPage",
                    fields=[
                        (
                            "page_ptr",
                            models.OneToOneField(
                                auto_created=True,
                                on_delete=django.db.models.deletion.CASCADE,
                                parent_link=True,
                                primary_key=True,
                                serialize=False,
                                to="wagtailcore.Page",
                            ),
                        ),
                        ("introduction", models.CharField(max_length=255)),
                    ],
                    options={
                        "db_table": "core_featureindexpage",
                    },
                    bases=("wagtailcore.page",),
                ),
                migrations.CreateModel(
                    name="FeatureIndexPageMenuOption",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        ("label", models.CharField(max_length=255)),
                    ],
                    options={
                        "db_table": "core_featureindexpagemenuoption",
                    },
                ),
                migrations.CreateModel(
                    name="FeaturePage",
                    fields=[
                        (
                            "page_ptr",
                            models.OneToOneField(
                                auto_created=True,
                                on_delete=django.db.models.deletion.CASCADE,
                                parent_link=True,
                                primary_key=True,
                                serialize=False,
                                to="wagtailcore.Page",
                            ),
                        ),
                        (
                            "social_text",
                            models.CharField(
                                blank=True,
                                help_text="Description of this page as it should appear when shared on social networks, or in Google results",
                                max_length=255,
                                verbose_name="Meta description",
                            ),
                        ),
                        (
                            "listing_intro",
                            models.TextField(
                                blank=True,
                                help_text="Summary of this page to display when this is linked from elsewhere in the site.",
                            ),
                        ),
                        ("introduction", models.CharField(max_length=255)),
                        (
                            "listing_image",
                            models.ForeignKey(
                                blank=True,
                                help_text="Image to display along with summary, when this page is linked from elsewhere in the site.",
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="+",
                                to="images.WagtailIOImage",
                            ),
                        ),
                        (
                            "social_image",
                            models.ForeignKey(
                                blank=True,
                                help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks",
                                null=True,
                                on_delete=django.db.models.deletion.SET_NULL,
                                related_name="+",
                                to="images.WagtailIOImage",
                                verbose_name="Meta image",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "core_featurepage",
                    },
                    bases=("wagtailcore.page", models.Model),
                ),
                migrations.CreateModel(
                    name="FeaturePageFeatureAspect",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "sort_order",
                            models.IntegerField(blank=True, editable=False, null=True),
                        ),
                        (
                            "feature_aspect",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="+",
                                to="features.FeatureAspect",
                            ),
                        ),
                        (
                            "page",
                            modelcluster.fields.ParentalKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name="feature_aspects",
                                to="features.FeaturePage",
                            ),
                        ),
                    ],
                    options={
                        "db_table": "core_featurepagefeatureaspect",
                    },
                ),
                migrations.AddField(
                    model_name="featureindexpagemenuoption",
                    name="link",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.Page",
                    ),
                ),
                migrations.AddField(
                    model_name="featureindexpagemenuoption",
                    name="page",
                    field=modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="secondary_menu_options",
                        to="features.FeatureIndexPage",
                    ),
                ),
                migrations.AddField(
                    model_name="bullet",
                    name="snippet",
                    field=modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bullets",
                        to="features.FeatureAspect",
                    ),
                ),
            ],
            database_operations=[],
        )
    ]
