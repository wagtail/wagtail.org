from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from wagtail_newsletter.models import NewsletterPageMixin

from wagtailio.newsletter.blocks import NewsletterContentBlock


@register_setting
class NewsletterSettings(BaseGenericSetting):
    footer = StreamField(NewsletterContentBlock(), blank=True, use_json_field=True)

    panels = [
        FieldPanel("footer"),
    ]


class NewsletterPage(NewsletterPageMixin, Page):
    date = models.DateField()
    preview = models.TextField(blank=True)
    body = StreamField(NewsletterContentBlock(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("preview"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.SearchField("body"),
    ]

    newsletter_template = "newsletter/newsletter_mjml.html"

    def get_newsletter_subject(self):
        if self.newsletter_subject:
            return self.newsletter_subject

        return f"This Week in Wagtail: {self.title}"

    def get_newsletter_context(self):
        context = super().get_newsletter_context()
        context["newsletter_settings"] = NewsletterSettings.load()
        return context

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["email_html"] = self.get_newsletter_html()
        return context


class NewsletterIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField()

    subpage_types = ["newsletter.NewsletterPage"]

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
