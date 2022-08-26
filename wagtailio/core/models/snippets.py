from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet

from wagtailio.core.blocks import GetStartedBlock, NavStreamField


@register_snippet
class GetStartedSnippet(models.Model):
    name = models.CharField(max_length=255)
    body = StreamField(
        [
            (
                "get_started_block",
                GetStartedBlock(),
            ),
        ],
        max_num=1,
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("body"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Get started block"


@register_snippet
class SignupFormSnippet(models.Model):
    name = models.CharField(
        max_length=255,
        help_text="For internal identification e.g 'This Week in Wagtail', 'TWIW'.",
    )
    heading = models.CharField(max_length=255)
    sub_heading = models.TextField(blank=True)
    mailchimp_account_id = models.CharField(
        verbose_name="Mailchimp Account ID", max_length=255, blank=True
    )
    mailchimp_newsletter_id = models.CharField(
        verbose_name="Mailchimp Newsletter ID", max_length=255, blank=True
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("heading"),
                FieldPanel("sub_heading"),
            ],
            "Title",
        ),
        MultiFieldPanel(
            [
                FieldPanel("mailchimp_account_id"),
                FieldPanel("mailchimp_newsletter_id"),
            ],
            "Mailchimp",
            classname="collapsible",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Signup form"


@register_snippet
class FooterMenuSnippet(models.Model):
    name = models.CharField(max_length=255)
    sections = StreamField(
        NavStreamField(),
    )

    panels = [
        FieldPanel("name"),
        StreamFieldPanel("sections"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Footer menu"
