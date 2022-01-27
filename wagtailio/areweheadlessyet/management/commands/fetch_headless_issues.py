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
        to_delete = []
        new_issues_count = 0
        for issue in issues:
            # Delete issue when it's closed.
            if (issue_number := issue["number"]) in issues_in_db and issue["state"] == "closed":
                to_delete.append(issue_number)
            else:
                _, created = WagtailHeadlessIssue.objects.update_or_create(
                    number=issue_number,
                    defaults={"title": issue["title"]},
                )
                if created:
                    new_issues_count += 1

        if not new_issues_count and not to_delete:
            self.stdout.write("No closed or new issues tagged #headless found.")
            return

        if new_issues_count:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {new_issues_count} new issue(s) tagged #headless."
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
