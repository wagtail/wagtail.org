from django.urls import path, reverse

from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from .views import ImageUsageReport


@hooks.register("register_reports_menu_item")
def register_image_usage_report_menu_item():
    return AdminOnlyMenuItem(
        "Image usage report",
        reverse("image_usage_report"),
        icon_name=ImageUsageReport.header_icon,
        order=700,
    )


@hooks.register("register_admin_urls")
def register_image_usage_report_url():
    return [
        path(
            "reports/image_usage_report/",
            ImageUsageReport.as_view(),
            name="image_usage_report",
        ),
        # Add a results-only view to add support for AJAX-based filtering
        path(
            "reports/image_usage_report/results/",
            ImageUsageReport.as_view(results_only=True),
            name="image_usage_report_results",
        ),
    ]
