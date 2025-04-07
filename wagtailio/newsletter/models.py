from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtail_newsletter.models import NewsletterPageMixin

from .blocks import NewsletterStoryBlock


class NewsletterPage(NewsletterPageMixin, Page):
    newsletter_template = "newsletter/newsletter_page_mjml.html"

    date = models.DateField("Newsletter date")
    issue_number = models.IntegerField(
        help_text="The issue number of the newsletter", default=0
    )
    preview_text = models.CharField(
        max_length=300,
        help_text="A short preview of the newsletter content that appears in email clients",
        blank=True,
    )

    content = StreamField(NewsletterStoryBlock(), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("issue_number"),
        FieldPanel("preview_text"),
        FieldPanel("content"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("content"),
        index.FilterField("date"),
        index.FilterField("issue_number"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.GET.get("email", "false") == "true":
            context["is_email"] = True

        return context


class NewsletterIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField()

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    @property
    def newsletters(self):
        # Get list of blog pages that are descendants of this page
        newsletters = NewsletterPage.objects.live().descendant_of(self)

        # Order by most recent date first
        newsletters = newsletters.order_by("-date")

        return newsletters

    def serve(self, request):
        # Get blogs
        newsletters = self.newsletters

        # Pagination
        page = request.GET.get("page")
        paginator = Paginator(newsletters, 5)  # Show 5 blogs per page
        try:
            newsletters = paginator.page(page)
        except PageNotAnInteger:
            newsletters = paginator.page(1)
        except EmptyPage:
            newsletters = paginator.page(paginator.num_pages)

        return render(
            request, self.template, {"self": self, "newsletters": newsletters}
        )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


class NewsletterEmailAddress(models.Model):
    email = models.EmailField()
    signed_up_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self) -> str:
        return f"NewsletterEmmail: {self.email}"
