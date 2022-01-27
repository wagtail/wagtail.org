import requests
from django.core.management.base import BaseCommand

from wagtailio.areweheadlessyet.models import WagtailHeadlessIssue


class Command(BaseCommand):
    help = "Fetch issues from Wagtail's repository tagged #headless."

    def handle(self, *args, **options):
        response = requests.get(
            "https://api.github.com/repos/wagtail/wagtail/issues",
            params={"labels": "headless"},
        )
        response.raise_for_status()

        issues = response.json()
        issues_in_db = set(
            WagtailHeadlessIssue.objects.values_list("number", flat=True)
        )
        to_delete, to_create = ([], [])
        for issue in issues:
            if (issue_number := issue["number"]) in issues_in_db:
                # Delete issue when it's closed.
                if issue["state"] == "closed":
                    to_delete.append(issue_number)
            else:
                to_create.append(
                    WagtailHeadlessIssue(
                        number=issue_number,
                        title=issue["title"],
                        url=issue["url"],
                    )
                )

        if not to_create and not to_delete:
            self.stdout.write("No closed or new issues tagged #headless found.")
            return

        if to_create:
            created = WagtailHeadlessIssue.objects.bulk_create(to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(created)} new issue(s) tagged #headless."
                )
            )

        if to_delete:
            deleted, _ = WagtailHeadlessIssue.objects.filter(
                number__in=to_delete
            ).delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully deleted {deleted} closed issue(s) tagged #headless."
                )
            )
