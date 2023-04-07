from typing import Dict, List

from django.db import models


class ManagerBase(models.Manager):
    def create_from_dict(self, dict_data: Dict, *args, **kwargs):
        """
        Create object based on dictionary.

        :param dict_data: data as dict
        :param args:
        :param kwargs:
        :return: created object
        """
        return self.create(**{**dict_data, **kwargs})

    def create_bulk_from_dict(self, dict_data_array: List[Dict], *args, **kwargs):
        """
        Create many objects as bulk based on list with dictionaries.

        :param dict_data_array: list with dictionaries
        :param args:
        :param kwargs:
        :return: list with created objects
        """

        return self.bulk_create(
            [self.model(**{**obj, **kwargs}) for obj in dict_data_array]
        )

    def get_or_create_obj(self, **kwargs):
        """
        Create of get instance. Return only object, excluding boolean whether the instance is created.

        :param kwargs: all arguments of instance to get
        :return: instance
        """

        obj, created = super().get_or_create(**kwargs)

        return obj
