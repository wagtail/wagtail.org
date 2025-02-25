from datetime import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand

import requests


class Command(BaseCommand):
    help = "Fetches newsletter URLs from the provided JSON file and saves them to the archive directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "input_file",
            type=str,
            help="Path to the JSON file containing newsletter data",
        )

    def handle(self, *args, **options):
        input_file = options["input_file"]

        # Read the JSON file
        try:
            with open(input_file) as f:
                newsletters = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Input file not found: {input_file}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"Invalid JSON in file: {input_file}"))
            return

        # Create output directory if it doesn't exist
        output_path = Path(__file__).resolve().parent.parent.parent / "archive"
        output_path.mkdir(parents=True, exist_ok=True)

        # Process each newsletter
        for newsletter in newsletters:
            url = newsletter.get("url")
            send_date = newsletter.get("send_date")
            title = newsletter.get("title")

            # Convert send_date to a datetime object
            date = datetime.fromisoformat(send_date.replace("Z", "+00:00"))
            # Create filename using date and title
            filename = f"{date.strftime('%Y-%m-%d')}_{title.replace(' ', '_')}.html"
            filepath = output_path / filename

            # Skip if file already exists
            if filepath.exists():
                self.stdout.write(f"File already exists, skipping: {filename}")
                continue

            # Fetch the newsletter content
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Save the content
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(response.text)

            self.stdout.write(self.style.SUCCESS(f"Successfully saved: {filename}"))

        self.stdout.write(self.style.SUCCESS("Newsletter fetching completed"))
