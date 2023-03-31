import uuid

from wagtailio.custom_base.models_abstract.abstract_log import AbstractLog
from django.db import models


class AbstractUuid(AbstractLog):
    uuid = models.UUIDField(
        "uuid", unique=True, editable=False, db_index=True, default=uuid.uuid4
    )

    class Meta(AbstractLog.Meta):
        abstract = True

    def __str__(self):
        return str(self.uuid)
