# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtailio.utils.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('images', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True, parent_link=True)),
                ('social_text', models.CharField(verbose_name='Meta description', help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True, max_length=255)),
                ('listing_intro', models.TextField(help_text='Summary of this page to display when this is linked from elsewhere in the site.', blank=True)),
                ('listing_image', models.ForeignKey(help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('social_image', models.ForeignKey(verbose_name='Meta image', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True, parent_link=True)),
                ('social_text', models.CharField(verbose_name='Meta description', help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True, max_length=255)),
                ('listing_intro', models.TextField(help_text='Summary of this page to display when this is linked from elsewhere in the site.', blank=True)),
                ('date', models.DateField()),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', wagtailio.utils.blocks.ImageFormatChoiceBlock())), label='Aligned image', icon='image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('imagequote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('alignment', wagtailio.utils.blocks.SimpleImageFormatChoiceBlock())), label='Image quote')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', wagtailio.utils.blocks.HTMLAlignmentChoiceBlock())), label='Raw HTML', icon='code')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('listing_image', models.ForeignKey(help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('main_image', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('social_image', models.ForeignKey(verbose_name='Meta image', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True, parent_link=True)),
                ('social_text', models.CharField(verbose_name='Meta description', help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True, max_length=255)),
                ('listing_intro', models.TextField(help_text='Summary of this page to display when this is linked from elsewhere in the site.', blank=True)),
                ('listing_image', models.ForeignKey(help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('social_image', models.ForeignKey(verbose_name='Meta image', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True, parent_link=True)),
                ('social_text', models.CharField(verbose_name='Meta description', help_text='Description of this page as it should appear when shared on social networks, or in Google results', blank=True, max_length=255)),
                ('listing_intro', models.TextField(help_text='Summary of this page to display when this is linked from elsewhere in the site.', blank=True)),
                ('body', wagtail.wagtailcore.fields.StreamField((('h2', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h3', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('h4', wagtail.wagtailcore.blocks.CharBlock(classname='title', icon='title')), ('intro', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow')), ('aligned_image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.RichTextBlock()), ('alignment', wagtailio.utils.blocks.ImageFormatChoiceBlock())), label='Aligned image', icon='image')), ('pullquote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False))))), ('imagequote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(classname='quote title')), ('attribution', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('alignment', wagtailio.utils.blocks.SimpleImageFormatChoiceBlock())), label='Image quote')), ('aligned_html', wagtail.wagtailcore.blocks.StructBlock((('html', wagtail.wagtailcore.blocks.RawHTMLBlock()), ('alignment', wagtailio.utils.blocks.HTMLAlignmentChoiceBlock())), label='Raw HTML', icon='code')), ('document', wagtail.wagtaildocs.blocks.DocumentChooserBlock(icon='doc-full-inverse'))))),
                ('listing_image', models.ForeignKey(help_text='Image to display along with summary, when this page is linked from elsewhere in the site.', blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('main_image', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
                ('social_image', models.ForeignKey(verbose_name='Meta image', help_text="Image to appear alongside 'Meta descro[topm', particularly for sharing on social networks", blank=True, on_delete=django.db.models.deletion.SET_NULL, to='images.WagtailIOImage', null=True, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
