from django.db import transaction
from django.shortcuts import render
from django.views import View

from wagtail.admin import messages

import requests

from .models import Grid, Package


def process(url="https://djangopackages.org/api/v4/grids/?q=wagtail"):
    grid_data = requests.get(url).json()
    for item in grid_data.get("results", []):
        title = item.get("title", "")
        if "wagtail" in title.lower():
            defaults = {key: item[key] for key in ["title", "slug", "description"]}
            grid, _ = Grid.objects.update_or_create(
                uid=item.get("id"), defaults=defaults
            )
            for url in item.get("packages", []):
                package_data = requests.get(url).json()
                defaults = {
                    key: package_data[key]
                    for key in [
                        "title",
                        "slug",
                        "repo_url",
                        "pypi_version",
                        "repo_forks",
                        "repo_description",
                        "pypi_url",
                        "documentation_url",
                        "repo_watchers",
                        "participants",
                    ]
                    if package_data[key] is not None
                }
                package, _ = Package.objects.update_or_create(
                    uid=package_data.get("id"), defaults=defaults
                )
                grid.packages.add(package)

    url = grid_data.get("next")
    if url:
        process(url)


class IndexView(View):
    http_method_names = ["get", "post"]

    def post(self, request):
        with transaction.atomic():
            # Start fresh, remove all m2m's.
            [grid.packages.clear() for grid in Grid.objects.all()]
            process()
            messages.success(request, "Success")
        return self.get(request)

    def get(self, request):
        return render(
            request,
            "packages/index.html",
            {},
        )
