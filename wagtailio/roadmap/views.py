from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from wagtail.admin import messages

from wagtailio.roadmap.forms import ImportForm
from wagtailio.roadmap.sync import RoadmapSyncError, process


class ImportView(FormView):
    template_name = "roadmap/import.html"
    form_class = ImportForm

    def form_valid(self, form):
        try:
            process(token=form.cleaned_data.get("github_token"))
        except RoadmapSyncError as e:
            messages.error(self.request, str(e))
            return redirect("roadmap:import")

        messages.success(
            self.request,
            "Successfully updated roadmap data from GitHub.",
            buttons=[
                messages.button(
                    reverse("wagtailsnippets_roadmap_milestone:list"), "View"
                )
            ],
        )
        return redirect("roadmap:import")
