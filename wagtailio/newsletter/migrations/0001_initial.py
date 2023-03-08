# Generated by Django 1.9.8 on 2016-07-28 10:33

import django.db.models.deletion
from django.db import migrations, models

import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0028_merge"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
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
                        ("email", models.EmailField(max_length=254)),
                    ],
                    options={
                        "db_table": "core_newsletteremailaddress",
                    },
                ),
                migrations.CreateModel(
                    name="NewsletterIndexPage",
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
                        ("intro", wagtail.fields.RichTextField(blank=True)),
                        ("body", wagtail.fields.RichTextField()),
                    ],
                    options={
                        "db_table": "core_newsletterindexpage",
                    },
                    bases=("wagtailcore.page",),
                ),
                migrations.CreateModel(
                    name="NewsletterPage",
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
                        ("date", models.DateField(verbose_name="Newsletter date")),
                        ("intro", wagtail.fields.RichTextField(blank=True)),
                        ("body", wagtail.fields.RichTextField()),
                    ],
                    options={
                        "db_table": "core_newsletterpage",
                    },
                    bases=("wagtailcore.page",),
                ),
            ],
            database_operations=[],
        )
    ]
