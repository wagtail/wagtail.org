from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Prefetch
from django.db.models.functions import Lower
from django.urls import reverse
from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from wagtailio.utils.models import CrossPageMixin, SocialMediaMixin


warning = """
    <p>
        Edit this data on Djangopackages.org.<br>
        `Settings > Django Packages > Import` will override this data.
    </p>
"""

readonly = forms.TextInput(attrs={"readonly": True})

default_about_text = " ".join(
    """
    <p>
        Projects listed on Wagtail.org are <i>third-party</i> packages.<br/>
        They are not vetted nor endorsed by Wagtail.<br/>
        Use them at your own risk.</p>
        <p>This page collects girds and packages from djangopackages.org.<br/>
        Please add or update Wagtail grids and Wagtail packages on djangopackages.org.
    </p>
""".split()
)  # Split/join to normalise whitespace


class PackagesPage(Page, SocialMediaMixin, CrossPageMixin):
    subtitle = models.CharField(max_length=255)
    about_title = models.CharField(max_length=255, default="About")
    about_text = RichTextField(
        default=default_about_text, features=["bold", "italic", "link"]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        packages = Package.objects.filter(publish=True).order_by(Lower("title"))
        context.update(
            {
                "grids": Grid.objects.filter(publish=True)
                .order_by(Lower("title"))
                .prefetch_related(Prefetch("packages", queryset=packages))
            }
        )
        return context

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("about_title"),
        FieldPanel("about_text"),
    ]


class Package(models.Model):
    publish = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    uid = models.IntegerField(
        unique=True, editable=False, help_text="The DjangoPackages.org id"
    )

    repo_url = models.URLField(blank=True)
    pypi_version = models.CharField(blank=True, max_length=255)
    repo_forks = models.IntegerField(null=True, blank=True)
    repo_description = models.TextField(blank=True)
    pypi_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    repo_watchers = models.IntegerField(null=True, blank=True)
    participants = ArrayField(models.CharField(max_length=255))

    panels = [
        FieldPanel("publish"),
        MultiFieldPanel(
            [
                HelpPanel(content=warning),
                FieldPanel("title", widget=readonly),
                FieldPanel("slug", widget=readonly),
                FieldPanel("repo_description", widget=readonly),
            ],
            heading="DjangoPackages.org data",
        ),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.pypi_url

    def get_admin_url(self):
        return reverse("packages_package_modeladmin_edit", args=(self.id,))

    def links(self):
        links = []
        if self.repo_url:
            links.append((self.repo_url, "Repo"))
        if self.pypi_url:
            links.append((self.pypi_url, "PyPi"))
        if self.documentation_url:
            links.append((self.documentation_url, "Docs"))
        return links


class Grid(models.Model):
    publish = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    uid = models.IntegerField(
        unique=True, editable=False, help_text="The DjangoPackages.org id"
    )
    packages = models.ManyToManyField(Package, blank=True)

    panels = [
        FieldPanel("publish"),
        MultiFieldPanel(
            [
                HelpPanel(content=warning),
                FieldPanel("title", widget=readonly),
                FieldPanel("slug", widget=readonly),
                FieldPanel("description", widget=readonly),
            ],
            heading="DjangoPackages.org data",
        ),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"https://djangopackages.org/grids/g/{self.slug}/"

    def get_admin_url(self):
        return reverse("packages_grid_modeladmin_edit", args=(self.id,))

    def display_title(self):
        return (
            self.title[8:].title() if self.title.startswith("Wagtail ") else self.title
        )
