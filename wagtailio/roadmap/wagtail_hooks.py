from django.urls import include, path, reverse
from django.utils.translation import gettext_lazy as _

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtailio.roadmap import views


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
