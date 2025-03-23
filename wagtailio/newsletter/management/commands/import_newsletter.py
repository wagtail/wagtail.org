from datetime import datetime
from pathlib import Path
import re

from django.core.management.base import BaseCommand, CommandError

from wagtail.models import Page
from wagtail.rich_text import RichText

from bs4 import BeautifulSoup

from wagtailio.newsletter.models import NewsletterPage


class Command(BaseCommand):
    help = "Import a newsletter HTML file into Wagtail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--html-file", required=True, help="Path to the HTML file to import"
        )
        parser.add_argument(
            "--parent-page-id",
            required=True,
            type=int,
            help="ID of the parent page to create the newsletter under",
        )

    def handle(self, *args, **options):
        html_file = Path(options["html_file"])
        if not html_file.exists():
            raise CommandError(f"File {html_file} does not exist")

        parent_page = Page.objects.get(id=options["parent_page_id"])

        # Parse the filename to get date and issue number
        filename = html_file.name
        match = re.match(r"(\d{4}-\d{2}-\d{2}).*?(?:#(\d+))?\.html", filename)
        if not match:
            raise CommandError(
                f"Could not parse date and issue number from filename {filename}"
            )

        date_str, issue_number = match.groups()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as error:
            raise CommandError(f"Could not parse date from {date_str}") from error

        issue_number = int(issue_number) if issue_number else 0

        # Parse the HTML file
        with html_file.open("r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        # Extract preview text
        preview_text = ""
        preview_elem = soup.find("span", class_="mcnPreviewText")
        if preview_elem:
            preview_text = preview_elem.text.strip()

        # Create the newsletter page
        title = f"This Week in Wagtail - Issue #{issue_number}"
        newsletter = NewsletterPage(
            title=title,
            slug=f"twiw-{date.strftime('%Y-%m-%d')}-{issue_number}",
            date=date,
            issue_number=issue_number,
            preview_text=preview_text,
        )

        # Build the content stream
        content = []

        # Find the main content area
        main_content = soup.find("td", class_="bodyCell")
        if main_content:
            # Process headings
            for heading in main_content.find_all(["h1", "h2"]):
                size = heading.name
                text = heading.text.strip()
                if text:
                    content.append(("heading", {"heading": text, "size": size}))

            # Process text content
            for p in main_content.find_all("p", class_=lambda x: x != "last-child"):
                text = str(p)
                if text.strip():
                    content.append(("content", {"text": RichText(text)}))

            # Process call to action buttons
            for button in main_content.find_all("a", class_="mceButton"):
                text = button.find_previous("p")
                text = text.text.strip() if text else ""
                content.append(
                    (
                        "call_to_action",
                        {
                            "text": text,
                            "url": button["href"],
                            "button_text": button.text.strip(),
                        },
                    )
                )

            # Process package list
            packages_section = main_content.find(
                "div", style=lambda x: x and "background-color:#2e1f5e" in x
            )
            if packages_section:
                packages = []
                for link in packages_section.find_all("a"):
                    text = link.text.strip()
                    # Try to parse package name and version
                    match = re.match(r"(.*?)\s+v([\d\.]+)", text)
                    if match:
                        name, version = match.groups()
                        packages.append(
                            {"name": name, "version": version, "url": link["href"]}
                        )

                if packages:
                    content.append(
                        ("package_list", {"title": "Packages", "packages": packages})
                    )

        # Set the content and save
        newsletter.content = content
        parent_page.add_child(instance=newsletter)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created newsletter {title}")
        )
