from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from . import views
from .viewsets import PackagesAdminGroup


@hooks.register("register_admin_viewset")
def register_viewset():
    return PackagesAdminGroup()


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("get-djangopackages/", views.IndexView.as_view(), name="package_index"),
    ]


@hooks.register("register_settings_menu_item")
def register_styleguide_menu_item():
    return MenuItem(
        "Django Packages", reverse("package_index"), icon_name="image", order=1000
    )
