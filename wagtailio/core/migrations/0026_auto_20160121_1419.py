# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtailio.utils.blocks
import wagtail.images.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.core.blocks
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('core', '0025_auto_20150701_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('body', wagtail.core.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='NewsletterPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('date', models.DateField(verbose_name='Newsletter date')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
                ('body', wagtail.core.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField((('h2', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('h3', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('h4', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('blockquote', wagtail.core.blocks.CharBlock(icon='openquote', classname='title')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('imagecaption', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock())), label='Image caption')), ('textimage', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock()), ('alignment', wagtailio.utils.blocks.SimpleImageFormatChoiceBlock())), icon='image')), ('colourtext', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('calltoaction', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('tripleimage', wagtail.core.blocks.StructBlock((('first_image', wagtail.images.blocks.ImageChooserBlock()), ('second_image', wagtail.images.blocks.ImageChooserBlock()), ('third_image', wagtail.images.blocks.ImageChooserBlock())), icon='image')), ('stats', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('stat', wagtail.core.blocks.CharBlock()), ('text', wagtail.core.blocks.CharBlock())), icon='code'))), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('markdown', wagtailio.utils.blocks.MarkDownBlock()), ('codeblock', wagtail.core.blocks.StructBlock((('language', wagtail.core.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('django', 'Django templating language'), ('html', 'HTML'), ('javascript', 'Javascript'), ('python', 'Python'), ('scss', 'SCSS')])), ('code', wagtail.core.blocks.TextBlock())))))),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='standardpage',
            name='body',
            field=wagtail.core.fields.StreamField((('h2', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('h3', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('h4', wagtail.core.blocks.CharBlock(icon='title', classname='title')), ('intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('blockquote', wagtail.core.blocks.CharBlock(icon='openquote', classname='title')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), ('imagecaption', wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.RichTextBlock())), label='Image caption')), ('textimage', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock()), ('alignment', wagtailio.utils.blocks.SimpleImageFormatChoiceBlock())), icon='image')), ('colourtext', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('calltoaction', wagtail.core.blocks.StructBlock((('text', wagtail.core.blocks.RichTextBlock()), ('background', wagtailio.utils.blocks.BackgroundColourChoiceBlock())), icon='pilcrow')), ('tripleimage', wagtail.core.blocks.StructBlock((('first_image', wagtail.images.blocks.ImageChooserBlock()), ('second_image', wagtail.images.blocks.ImageChooserBlock()), ('third_image', wagtail.images.blocks.ImageChooserBlock())), icon='image')), ('stats', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock((('image', wagtail.images.blocks.ImageChooserBlock()), ('stat', wagtail.core.blocks.CharBlock()), ('text', wagtail.core.blocks.CharBlock())), icon='code'))), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='code')), ('markdown', wagtailio.utils.blocks.MarkDownBlock()), ('codeblock', wagtail.core.blocks.StructBlock((('language', wagtail.core.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('django', 'Django templating language'), ('html', 'HTML'), ('javascript', 'Javascript'), ('python', 'Python'), ('scss', 'SCSS')])), ('code', wagtail.core.blocks.TextBlock())))))),
            preserve_default=True,
        ),
    ]
