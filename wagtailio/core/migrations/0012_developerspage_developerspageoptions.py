import django.db.models.deletion
import modelcluster.fields
import wagtail.fields

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0015_add_more_verbose_names"),
        ("images", "__first__"),
        ("core", "0011_remove_standardpage_main_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="DevelopersPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        to="wagtailcore.Page",
                        serialize=False,
                        primary_key=True,
                        parent_link=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "social_text",
                    models.CharField(
                        blank=True,
                        verbose_name="Meta description",
                        max_length=255,
                        help_text="Description of this page as it should appear when shared on social networks, or in Google results",
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
                ("body_heading", models.CharField(max_length=255)),
                ("body", wagtail.fields.RichTextField()),
                (
                    "listing_image",
                    models.ForeignKey(
                        to="images.WagtailIOImage",
                        blank=True,
                        null=True,
                        help_text="Image to display along with summary, when this page is linked from elsewhere in the site.",
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                    ),
                ),
                (
                    "social_image",
                    models.ForeignKey(
                        to="images.WagtailIOImage",
                        blank=True,
                        verbose_name="Meta image",
                        null=True,
                        help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks",
                        related_name="+",
                        on_delete=django.db.models.deletion.SET_NULL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", models.Model),
        ),
        migrations.CreateModel(
            name="DevelopersPageOptions",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        serialize=False,
                        verbose_name="ID",
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "icon",
                    models.CharField(
                        max_length=255,
                        choices=[
                            ("\x0c09b", "Github"),
                            ("\x0c1a0", "Google"),
                            ("\x0c06e", "Eye"),
                            ("\x0c233", "Servers"),
                        ],
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("summary", models.CharField(max_length=255)),
                (
                    "external_link",
                    models.URLField(blank=True, verbose_name="External link"),
                ),
                (
                    "internal_link",
                    models.ForeignKey(
                        to="wagtailcore.Page",
                        blank=True,
                        null=True,
                        related_name="+",
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        to="core.DevelopersPage", related_name="options"
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
            bases=(models.Model,),
        ),
    ]
