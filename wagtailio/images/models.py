from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from wagtail.wagtailimages.models import AbstractImage, AbstractRendition


class WagtailIOImage(AbstractImage):
    alternative_text = models.CharField(max_length=255, blank=True, help_text="The alternative text for the image, provided for the benefit of visually impaired users")
    admin_form_fields = (
        'title',
        'file',
        'tags',
        'focal_point_x',
        'focal_point_y',
        'focal_point_width',
        'focal_point_height',
    )


class WagtailIORendition(AbstractRendition):
    image = models.ForeignKey('WagtailIOImage', related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter', 'focal_point_key'),
        )


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=WagtailIOImage)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=WagtailIORendition)
def rendition_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
