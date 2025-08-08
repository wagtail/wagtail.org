from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from wagtail.models import Page, Site


class Command(BaseCommand):
    help = "Load initial data for the Wagtail.org project"

    @transaction.atomic
    def handle(self, *args, **options):
        Site.objects.all().delete()
        Page.objects.all().delete()
        Permission.objects.all().delete()
        Group.objects.all().delete()
        ContentType.objects.all().delete()

        call_command("loaddata", "initial_data")
        self.stdout.write(self.style.SUCCESS("Successfully loaded initial data"))
