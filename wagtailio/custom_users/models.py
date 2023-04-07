from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from wagtailio.custom_base.models_abstract.abstract_uuid import AbstractUuid
from wagtailio.custom_users.managers.manager_user import ManagerUser


class User(AbstractBaseUser, PermissionsMixin, AbstractUuid):
    email = models.EmailField(_("email address"), unique=True)

    first_name = models.CharField(
        _("first name"), max_length=150, null=False, blank=True, default=""
    )
    last_name = models.CharField(
        _("last name"), max_length=150, null=False, blank=True, default=""
    )

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)
    is_manager = models.BooleanField(_("manager"), default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)

    last_login = models.DateTimeField(_("last login"), default=now)
    date_joined = models.DateTimeField(_("date joined"), default=now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ManagerUser()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

        ordering = ["-modified"]
