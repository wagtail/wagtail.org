from functools import cached_property

from django import forms
from django.db import models
from django.template.defaultfilters import date

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page, index

from wagtailio.core.blocks import ContentStoryBlock
from wagtailio.utils.models import SocialMediaMixin

github_help = "To change this data, edit the corresponding item on GitHub and then synchronise from Wagtail settings"

readonly = forms.TextInput(attrs={"readonly": True})


class State(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"


class RoadmapPage(Page, SocialMediaMixin):
    parent_page_types = ["core.HomePage"]
    subpage_types = []

    intro = RichTextField(
        verbose_name="Intro",
        blank=True,
        features=["bold", "italic", "link"],
    )
    sponsorship_page = models.ForeignKey(
        "core.ContentPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="This will be used as the default link for the 'Sponsor this' label",
    )
    fine_print = RichTextField(blank=True)
    body = StreamField(ContentStoryBlock())

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("sponsorship_page"),
        FieldPanel("fine_print"),
        FieldPanel("body"),
    ]

    promote_panels = Page.promote_panels + SocialMediaMixin.panels

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.SearchField("fine_print"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        items = MilestoneItem.objects.order_by("sort_order")
        context.update(
            {
                "milestones": Milestone.objects.filter(state=State.OPEN)
                .order_by(models.F("due_on").asc(nulls_last=True))
                .prefetch_related(models.Prefetch("items", queryset=items))
            }
        )
        return context


class MilestoneItem(Orderable):
    NEEDS_SPONSORSHIP_LABEL = "needs sponsorship"

    sponsorship_url = models.URLField(
        blank=True,
        verbose_name="Sponsorship URL",
        help_text="Custom URL to use for the 'Sponsor this' label",
    )
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
        FieldPanel("sponsorship_url"),
        MultiFieldPanel(
            [
                FieldPanel("title", widget=readonly),
                FieldPanel("url", widget=readonly),
                FieldPanel("labels", widget=readonly),
            ],
            heading="GitHub data (read-only)",
            help_text=github_help,
        ),
    ]

    class Meta:
        verbose_name = "roadmap milestone item"
        verbose_name_plural = "roadmap milestone items"
        ordering = ["sort_order"]

    def __str__(self):
        return self.title

    def clean(self):
        self.labels = ",".join(self.labels_set)

    @cached_property
    def labels_set(self):
        # Return an empty set if labels string is empty, to avoid returning {""}
        return set(self.labels.split(",")) - {""}

    @cached_property
    def labels_list(self):
        return sorted(self.labels_set - {self.NEEDS_SPONSORSHIP_LABEL}, key=str.lower)

    @cached_property
    def needs_sponsorship(self):
        return self.NEEDS_SPONSORSHIP_LABEL in self.labels_set


class Milestone(ClusterableModel):
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
        MultiFieldPanel(
            [
                FieldPanel("title", widget=readonly),
                FieldPanel("url", widget=readonly),
            ],
            heading="GitHub data (read-only)",
            help_text=github_help,
        ),
        InlinePanel("items", heading="Items", label="Item"),
    ]

    class Meta:
        verbose_name = "roadmap milestone"
        verbose_name_plural = "roadmap milestones"
        ordering = ["-due_on"]

    @cached_property
    def display_title(self):
        # Special case: Future
        if not self.due_on:
            return self.title
        # e.g. August 2022
        return date(self.due_on, "F Y")

    display_title.admin_order_field = "due_on"
    display_title.short_description = "Due on"

    @cached_property
    def display_subtitle(self):
        # Special case: Future has no subtitle
        if not self.due_on:
            return ""
        # e.g. v5.0
        return self.title

    def get_admin_url(self):
        return AdminURLFinder().get_edit_url(self)

    def __str__(self):
        return f"{self.display_title} - {self.display_subtitle}".strip(" -")
