from django.conf import settings
from django.core.management.base import BaseCommand

from mailchimp3 import MailChimp

from wagtailio.newsletter.models import NewsletterIndexPage, NewsletterPage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--index-page-id",
            nargs=1,
            type=int,
            dest="index_page_id",
            help="The ID of the NewsletterIndexPage to add the new pages to",
        )

    def handle(self, **options):
        client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY)

        campaigns = client.campaigns.all(
            get_all=True,
            fields="campaigns.id,campaigns.settings.title,campaigns.send_time",
        )

        if options["index_page_id"]:
            try:
                index_page = NewsletterIndexPage.objects.get(
                    id=options["index_page_id"][0]
                )
            except NewsletterIndexPage.DoesNotExist:
                print(
                    "NewsletterIndexPage with ID {} does not exist".format(
                        options["index_page_id"]
                    )
                )
                index_page = None
        else:
            index_page = NewsletterIndexPage.objects.live().public().first()

        if index_page:
            for campaign in campaigns["campaigns"]:
                content = client.campaigns.content.get(campaign["id"])
                existing_page = NewsletterPage.objects.filter(
                    mailchimp_campaign_id=campaign["id"]
                ).last()

                if not existing_page:
                    # check if the campaign has a title, content, send time
                    if (
                        "html" in content.keys()
                        and "send_time" in campaign.keys()
                        and campaign["send_time"] != ""
                        and "title" in campaign["settings"].keys()
                        and campaign["settings"]["title"]
                    ):
                        newsletter_page = NewsletterPage(
                            title=campaign["settings"]["title"],
                            mailchimp_campaign_id=campaign["id"],
                            mailchimp_campaign_content=content["html"],
                            first_published_at=campaign["send_time"],
                            date=campaign["send_time"].split("T")[0],
                        )
                        index_page.add_child(instance=newsletter_page)
                        newsletter_page.save()

                        print(
                            "Created new page for {}".format(
                                campaign["settings"]["title"]
                            )
                        )
