from datetime import datetime
import os
from pathlib import Path

from django.core.management.base import BaseCommand

from mailchimp_marketing import Client
import requests


def get_mailchimp_client():
    """Initialize and return a Mailchimp client."""
    api_key = os.getenv("MAILCHIMP_API_KEY")
    if not api_key:
        raise ValueError("MAILCHIMP_API_KEY environment variable is not set")

    # Extract datacenter from API key (it's the part after the '-')
    datacenter = api_key.split("-")[-1]

    client = Client()
    client.set_config({"api_key": api_key, "server": datacenter})
    client.ping.get()
    return client


def fetch_campaign_urls():
    """Fetch all campaign URLs from Mailchimp."""
    client = get_mailchimp_client()

    campaigns = []
    offset = 0
    count = 100  # Number of campaigns to fetch per request

    while True:
        # Get a batch of campaigns
        response = client.campaigns.list(
            count=count,
            offset=offset,
            fields=[
                "campaigns.archive_url",
                "campaigns.settings.title",
                "campaigns.send_time",
                "campaigns.id",
                "total_items",
            ],
        )

        # Extract campaign data
        for campaign in response["campaigns"]:
            # Only include campaigns that have been sent
            if campaign.get("send_time"):
                campaigns.append(
                    {
                        "id": campaign["id"],
                        "send_date": campaign["send_time"],
                        "title": campaign["settings"]["title"],
                        "url": campaign["archive_url"],
                    }
                )

        # Check if we've fetched all campaigns
        total_items = response["total_items"]
        offset += count
        if offset >= total_items:
            break

    # Sort campaigns by send date, newest first
    campaigns.sort(key=lambda x: x["send_date"], reverse=True)
    return campaigns


class Command(BaseCommand):
    help = "Fetches newsletters from Mailchimp and saves them to the archive directory"

    def handle(self, *args, **options):
        # Create output directory if it doesn't exist
        output_path = Path(__file__).resolve().parent.parent.parent / "archive"
        output_path.mkdir(parents=True, exist_ok=True)

        cutoff_date = datetime.fromisoformat("2023-07-20")

        # Process each newsletter
        for newsletter in fetch_campaign_urls():
            url = newsletter.get("url")
            send_date = newsletter.get("send_date")
            title = newsletter.get("title")

            # Convert send_date to a datetime object
            date = datetime.fromisoformat(send_date.replace("Z", "+00:00"))

            # Skip if newsletter is older than cutoff date
            if date.date() < cutoff_date.date():
                continue

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
