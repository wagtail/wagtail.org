from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Grid
from ...views import process


class Command(BaseCommand):
    help = "Import grids and packages from Djangopackages.org"

    def handle(self, *args, **options):
        with transaction.atomic():
            # Start fresh, remove all m2m's.
            [grid.packages.clear() for grid in Grid.objects.all()]
            process()
