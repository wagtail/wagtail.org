from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save


class ManagerUser(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_manager", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(email, password, **extra_fields)

    def bulk_create(self, objs, **kwargs):
        db_objects = super().bulk_create(objs, **kwargs)

        for obj in objs:
            post_save.send(obj.__class__, instance=obj, created=True)

        return db_objects

    def filter(self, *args, **kwargs):
        """
        Exclude superusers on filtering
        """
        return super().filter(*args, **kwargs)
