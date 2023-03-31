from wagtailio.custom_base.models_abstract.abstract_base import AbstractBase
from django.db import models


class AbstractLog(AbstractBase):
    created = models.DateTimeField("created", auto_now_add=True)
    modified = models.DateTimeField("modified", auto_now=True)

    class Meta(AbstractBase.Meta):
        abstract = True
