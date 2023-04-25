from django import forms
from django.db import models
from django.template.defaultfilters import date
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet


warning = """
Control whether this item should be published.
To change other data, edit the corresponding item on GitHub
and go to Settings > Roadmap > Import to synchronise.
"""

readonly = forms.TextInput(attrs={"readonly": True})


class State(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"


class Item(models.Model):
    NEEDS_SPONSORSHIP_LABEL = "needs sponsorship"

    publish = models.BooleanField(default=True)
    needs_sponsorship = models.BooleanField(default=False, editable=False)
    number = models.IntegerField(
        unique=True,
        editable=False,
        help_text="GitHub issue number",
    )
    state = models.CharField(choices=State.choices, max_length=32, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField(verbose_name="URL")
    milestone = ParentalKey(
        "roadmap.Milestone",
        on_delete=models.CASCADE,
        related_name="items",
    )
    # For simplicity, store labels as a comma-separated text
    labels = models.TextField(help_text="Comma-separated list of labels", blank=True)

    panels = [
        FieldPanel("publish", help_text=warning),
        MultiFieldPanel(
            [
                FieldPanel("title", widget=readonly),
                FieldPanel("url", widget=readonly),
                FieldPanel("labels", widget=readonly),
            ],
            heading="GitHub data",
        ),
    ]

    class Meta:
        verbose_name = _("roadmap item")
        verbose_name_plural = _("roadmap items")

    def __str__(self):
        return self.title

    def clean(self):
        labels = set(self.labels.split(","))
        self.needs_sponsorship = self.NEEDS_SPONSORSHIP_LABEL in labels
        labels -= {self.NEEDS_SPONSORSHIP_LABEL, ""}
        self.labels = ",".join(sorted(labels))


@register_snippet
class Milestone(ClusterableModel):
    publish = models.BooleanField(default=True)
    number = models.IntegerField(
        unique=True,
        editable=False,
        help_text="GitHub milestone number",
    )
    state = models.CharField(choices=State.choices, max_length=32, editable=False)
    due_on = models.DateField(null=True, blank=True, editable=False)
    title = models.CharField(max_length=255)
    url = models.URLField(verbose_name="URL")

    panels = [
        FieldPanel("publish", help_text=warning),
        MultiFieldPanel(
            [
                FieldPanel("title", widget=readonly),
                FieldPanel("url", widget=readonly),
            ],
            heading="GitHub data",
        ),
        InlinePanel("items", heading="Items", label="Item"),
    ]

    class Meta:
        verbose_name = _("roadmap milestone")
        verbose_name_plural = _("roadmap milestones")
        ordering = ["-due_on"]

    @property
    def display_title(self):
        # Special case: Future
        if not self.due_on:
            return self.title
        # e.g. August 2022
        return date(self.due_on, "F Y")

    @property
    def display_subtitle(self):
        # Special case: Future has no subtitle
        if not self.due_on:
            return ""
        # e.g. v5.0
        return self.title

    def __str__(self):
        return f"{self.display_title} - {self.display_subtitle}".strip(" -")
