# Generated by Django 2.2.13 on 2021-03-12 04:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtailio.services.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_add_divider_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicespage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(form_classname='full title', required=True)), ('content', wagtail.core.blocks.StreamBlock([('subheading', wagtailio.services.blocks.SubheadingBlock()), ('divider', wagtailio.services.blocks.DividerBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock(features=["bold", "italic", "link",  "ul", "ol"]))], form_classname='full', required=False))]))], blank=True, null=True),
        ),
    ]