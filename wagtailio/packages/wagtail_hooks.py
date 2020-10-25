from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from . import views
from .models import Grid, Package


class GridAdmin(ModelAdmin):
    model = Grid
    menu_icon = "doc-full-inverse"
    list_display = ["title", "publish"]
    list_filter = ["publish"]
    search_fields = ["title"]


class PackageAdmin(ModelAdmin):
    model = Package
    menu_icon = "doc-full-inverse"
    list_display = ["title", "publish"]
    list_filter = ["publish"]
    search_fields = ["title"]


class PackagesAdminGroup(ModelAdminGroup):
    menu_label = "Package"
    menu_icon = "folder-open-inverse"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = [GridAdmin, PackageAdmin]


modeladmin_register(PackagesAdminGroup)


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("get-djangopackages/", views.IndexView.as_view(), name="package_index"),
    ]


@hooks.register("register_settings_menu_item")
def register_styleguide_menu_item():
    return MenuItem(
        _("Django Packages"), reverse("package_index"), icon_name="image", order=1000
    )
