from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtailio.roadmap import views
from wagtailio.roadmap.models import Milestone


@hooks.register("register_admin_urls")
def register_admin_urls():
    urlpatterns = [
        path("get-roadmap/", views.ImportView.as_view(), name="import"),
    ]
    return [path("", include((urlpatterns, "roadmap"), "roadmap"))]


@hooks.register("register_settings_menu_item")
def register_roadmap_menu_item():
    return MenuItem(
        _("GitHub Roadmap"),
        reverse("roadmap:import"),
        icon_name="crosshairs",
        order=1100,
    )


class MilestoneViewSet(SnippetViewSet):
    def get_url_name(self, view_name):
        if view_name == "add":
            return "roadmap:import"
        return super().get_url_name(view_name)


register_snippet(Milestone, viewset=MilestoneViewSet)
