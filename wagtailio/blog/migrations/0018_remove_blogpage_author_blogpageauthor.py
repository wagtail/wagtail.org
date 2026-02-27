from django.db import migrations, models
import django.db.models.deletion

import modelcluster.fields


def copy_authors(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    BlogPageAuthor = apps.get_model("blog", "BlogPageAuthor")

    for page in BlogPage.objects.exclude(author__isnull=True):
        BlogPageAuthor.objects.create(
            page=page,
            author=page.author,
        )


def reverse_copy_authors(apps, schema_editor):
    BlogPage = apps.get_model("blog", "BlogPage")
    BlogPageAuthor = apps.get_model("blog", "BlogPageAuthor")

    for page in BlogPage.objects.all():
        first = BlogPageAuthor.objects.filter(page=page).first()
        if first:
            page.author = first.author
            page.save()


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0017_alter_blogpage_body"),
    ]

    operations = [
        # 1. Create the new through model first
        migrations.CreateModel(
            name="BlogPageAuthor",
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
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="blog.author",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="authors",
                        to="blog.blogpage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        # 2. Copy data before removing the old field
        migrations.RunPython(copy_authors, reverse_copy_authors),
        # 3. Now it's safe to drop the old field
        migrations.RemoveField(
            model_name="blogpage",
            name="author",
        ),
    ]
