# Generated by Django 2.2.13 on 2021-03-12 09:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailio.services.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_add_link_button_to_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicespage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(form_classname='full title', required=True)), ('content', wagtail.core.blocks.StreamBlock([('subheading', wagtailio.services.blocks.SubheadingBlock()), ('divider', wagtailio.services.blocks.DividerBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ul', 'ol'])), ('card_section', wagtail.core.blocks.StreamBlock([('card', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic'], required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))])), ('link_button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock(features=['bold'], required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))]))], required=False))]))], blank=True, null=True),
        ),
    ]
