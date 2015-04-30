# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import utils.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks
import wagtail.wagtaildocs.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('images', '__first__'),
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('home', '0004_auto_20150430_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', serialize=False, primary_key=True, auto_created=True)),
                ('social_text', models.CharField(max_length=255, blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results')),
                ('listing_intro', models.TextField(blank=True)),
                ('listing_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('social_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', serialize=False, primary_key=True, auto_created=True)),
                ('social_text', models.CharField(max_length=255, blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results')),
                ('listing_intro', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', utils.blocks.ImageFormatChoiceBlock())), label='Aligned image', icon='image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('imagequote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('alignment', utils.blocks.SimpleImageFormatChoiceBlock())), label='Image quote')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', utils.blocks.HTMLAlignmentChoiceBlock())), label='Raw HTML', icon='code')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('listing_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('main_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('social_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', serialize=False, primary_key=True, auto_created=True)),
                ('social_text', models.CharField(max_length=255, blank=True, help_text='Description of this page as it should appear when shared on social networks, or in Google results')),
                ('listing_intro', models.TextField(blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', utils.blocks.ImageFormatChoiceBlock())), label='Aligned image', icon='image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('imagequote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('alignment', utils.blocks.SimpleImageFormatChoiceBlock())), label='Image quote')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', utils.blocks.HTMLAlignmentChoiceBlock())), label='Raw HTML', icon='code')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('listing_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('main_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('social_image', models.ForeignKey(to='images.WagtailIOImage', blank=True, null=True, help_text="Image to appear alongside 'social text', particularly for sharing on social networks", on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
