from wagtailio.custom_base.managers.manager_base import ManagerBase
from django.db import models
from django.core.exceptions import FieldDoesNotExist
from modelcluster.models import ClusterableModel


class AbstractBase(ClusterableModel, models.Model):
    objects = ManagerBase()

    panels = []

    def update(self, *args, **kwargs):
        """
        Kwargs arguments can overwrite instance attributes.

        :param args:
        :param kwargs:
        :return: updated instance
        """

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.save()

        return self

    @staticmethod
    def add_id_tag_to_foreign_key(field):
        """
        Add id tag to field name if field is relational field.

        :param field: model field object
        :return: field name with id
        """

        if field.get_internal_type() in ["ForeignKey", "ParentalKey"]:
            return "{}_id".format(field.name)

        return field.name

    @classmethod
    def get_field_names(
        cls, include_primary_key=True, add_foreign_id_tag=False, include_m2m=False
    ):
        """
        Get all field names.

        :param include_primary_key: whether 'id' is included as field
        :param add_foreign_id_tag: whether '_id' suffix is used on relational fields
        :param include_m2m: whether many2many fields are included
        :return: list with all field names
        """

        m2m_fields = cls._meta.many_to_many if include_m2m else ()

        return [
            cls.add_id_tag_to_foreign_key(field) if add_foreign_id_tag else field.name
            for field in cls._meta.fields + m2m_fields
            if include_primary_key or not field.primary_key
        ]

    @classmethod
    def get_field_names_foreign(cls):
        field_names_foreign = []

        for field_name in cls.get_field_names():
            if cls.get_field_type(field_name) in ["ForeignKey", "ParentalKey"]:
                field_names_foreign.append(field_name)

        return field_names_foreign

    @classmethod
    def get_field(cls, field_name):
        """
        Get model field object based on field name.

        :param field_name: field name
        :return: model field object
        """

        return cls._meta.get_field(field_name)

    @classmethod
    def get_foreign_key_model(cls, field_name):
        """
        Get model of foreign key based on field name.

        :param field_name: field name
        :return: foreign key model
        """

        return cls._meta.get_field(field_name).remote_field.model

    @classmethod
    def get_field_type(cls, field_name):
        """
        Get type of field based on field name.

        :param field_name: field name
        :return: field type
        """

        return cls.get_field(field_name).get_internal_type()

    @classmethod
    def has_field(cls, field_name):
        """
        Check whether model has field based on field name.

        :param field_name: field name
        :return: True if model has field
        """

        try:
            cls.get_field(field_name)
        except FieldDoesNotExist:
            return False

        return True

    @classmethod
    def is_abstract(cls):
        """
        Get whether model is abstract.

        :return: True if model is abstract
        """

        return bool(cls._meta.abstract)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)
