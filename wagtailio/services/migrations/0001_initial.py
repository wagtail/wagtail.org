# Generated by Django 2.2.13 on 2021-06-16 18:35

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailio.services.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, null=True)),
                ('body', wagtail.core.fields.StreamField([('section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(form_classname='full title', required=True)), ('icon', wagtail.core.blocks.ChoiceBlock(choices=[('astronaut', 'Astronaut'), ('cloud', 'Cloud'), ('money-check', 'Money check'), ('tools', 'Tools')], required=False)), ('section_media', wagtailio.services.blocks.SectionMediaBlock(required=False)), ('section_image', wagtail.images.blocks.ImageChooserBlock(help_text='Section image is used as a fallback when no media is defined.', required=False)), ('section_image_caption', wagtail.core.blocks.CharBlock(help_text='Rendered below the image/media', label='Section image/media caption', required=False)), ('content', wagtail.core.blocks.StreamBlock([('subheading', wagtailio.services.blocks.SubheadingBlock()), ('divider', wagtailio.services.blocks.DividerBlock()), ('paragraph', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'ul', 'ol'])), ('cards', wagtailio.services.blocks.CardsBlock()), ('link_button', wagtail.core.blocks.StructBlock([('lead_text', wagtail.core.blocks.CharBlock(help_text='Text leading up the action text of the button.', max_length=50, required=False)), ('action_text', wagtail.core.blocks.CharBlock(help_text='Emphasised text for the button action.', max_length=50, required=True)), ('link', wagtail.core.blocks.URLBlock(required=True))])), ('quote', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.TextBlock(required=True)), ('source', wagtail.core.blocks.CharBlock(required=True)), ('reference', wagtail.core.blocks.CharBlock(help_text='Additional information about the source. E.g. a persons job title and company.', required=False))]))], required=False))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
