# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-29 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtailio.utils.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0028_merge'),
        ('core', '0031_auto_20160728_1315'),
        ('images', '0004_auto_20160727_1108'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                 migrations.CreateModel(
                    name='Author',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=255)),
                        ('job_title', models.CharField(blank=True, max_length=255)),
                        ('url', models.URLField(blank=True)),
                        ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage')),
                    ],
                    options={
                        'db_table': 'core_author',
                    },
                ),
                migrations.CreateModel(
                    name='BlogIndexPage',
                    fields=[
                        ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                        ('social_text', models.CharField(blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results', max_length=255, verbose_name='Meta description')),
                        ('listing_intro', models.TextField(blank=True, help_text='Summary of this page to display when this is linked from elsewhere in the site.')),
                        ('listing_image', models.ForeignKey(blank=True, help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage')),
                        ('social_image', models.ForeignKey(blank=True, help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage', verbose_name='Meta image')),
                    ],
                    options={
                        'db_table': 'core_blogindexpage',
                    },
                    bases=('wagtailcore.page', models.Model),
                ),
                migrations.CreateModel(
                    name='BlogPage',
                    fields=[
                        ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                        ('social_text', models.CharField(blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results', max_length=255, verbose_name='Meta description')),
                        ('listing_intro', models.TextField(blank=True, help_text='Summary of this page to display when this is linked from elsewhere in the site.')),
                        ('date', models.DateField()),
                        ('introduction', models.CharField(max_length=511)),
                        ('body', wagtail.fields.StreamField((('h2', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.blocks.RichTextBlock(icon='pilcrow')), ('blockquote', wagtail.blocks.CharBlock(classname='title', icon='openquote')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('imagecaption', wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.RichTextBlock())), label='Image caption')), ('textimage', wagtail.blocks.StructBlock((('text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock()), ('alignment', wagtailio.utils.blocks.SimpleImageFormatChoiceBlock())), icon='image')), ('colourtext', wagtail.blocks.StructBlock((('text', wagtail.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('calltoaction', wagtail.blocks.StructBlock((('text', wagtail.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('tripleimage', wagtail.blocks.StructBlock((('first_image', wagtail.images.blocks.ImageChooserBlock()), ('second_image', wagtail.images.blocks.ImageChooserBlock()), ('third_image', wagtail.images.blocks.ImageChooserBlock())), icon='image')), ('stats', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('stat', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.CharBlock())), icon='code'))), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('markdown', wagtailio.utils.blocks.MarkDownBlock()), ('codeblock', wagtail.blocks.StructBlock((('language', wagtail.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('django', 'Django templating language'), ('html', 'HTML'), ('javascript', 'Javascript'), ('python', 'Python'), ('scss', 'SCSS')])), ('code', wagtail.blocks.TextBlock()))))))),
                        ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.Author')),
                        ('listing_image', models.ForeignKey(blank=True, help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage')),
                        ('main_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage')),
                        ('social_image', models.ForeignKey(blank=True, help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.WagtailIOImage', verbose_name='Meta image')),
                    ],
                    options={
                        'db_table': 'core_blogpage',
                    },
                    bases=('wagtailcore.page', models.Model),
                ),
            ],
            database_operations=[],
        )
    ]
