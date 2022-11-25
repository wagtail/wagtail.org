from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class NewsletterPage(Page):
    date = models.DateField("Newsletter date")
    intro = RichTextField(blank=True)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
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
