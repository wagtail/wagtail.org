from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


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

    class Meta:
        verbose_name = _("roadmap milestone")
        verbose_name_plural = _("roadmap milestones")
        ordering = ["-due_on"]
