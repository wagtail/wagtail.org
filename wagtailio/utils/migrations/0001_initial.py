from django.db import migrations, models

import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0015_add_more_verbose_names"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkGroupLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        verbose_name="ID",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, null=True, editable=False),
                ),
                (
                    "link_URL",
                    models.URLField(help_text="Choose a URL to which to link"),
                ),
                ("link_text", models.TextField(help_text="Text of the link")),
                (
                    "link_description",
                    models.TextField(blank=True, help_text="Optional"),
                ),
                (
                    "link_icon",
                    models.TextField(
                        max_length=50,
                        blank=True,
                        null=True,
                        help_text="Optional. The code of a Fontawesome icon to display beside this link e.g fa-twitter",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["sort_order"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="LinkGroupSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        verbose_name="ID",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "verbose_name": "Link group",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="MenuSnippet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        verbose_name="ID",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "menu_name",
                    models.CharField(
                        max_length=255,
                        help_text="The name of the menu for internal identification e.g 'Primary', 'Footer'.",
                    ),
                ),
            ],
            options={
                "ordering": ["menu_name"],
                "verbose_name": "Menu",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="MenuSnippetLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        verbose_name="ID",
                        serialize=False,
                        primary_key=True,
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, null=True, editable=False),
                ),
                (
                    "link_text",
                    models.TextField(
                        blank=True,
                        help_text="Optional. Override title text for chosen link page",
                    ),
                ),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        help_text="Choose a page to which to link",
                        to="wagtailcore.Page",
                        related_name="+",
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "snippet",
                    modelcluster.fields.ParentalKey(
                        to="utils.MenuSnippet", related_name="links"
                    ),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["sort_order"],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="linkgrouplink",
            name="snippet",
            field=modelcluster.fields.ParentalKey(
                to="utils.LinkGroupSnippet", related_name="links"
            ),
            preserve_default=True,
        ),
    ]
