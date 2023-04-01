from django.conf.urls import url
from django.urls import path

from .views.api_view_dashboard_overview import ApiViewDashboardOverview
from .views.view_main import ViewDashboardIndex

urlpatterns = [
    url(r"^$", ViewDashboardIndex.as_view(), name="dashboard_main"),
    url(
        r"^api/overview/$",
        ApiViewDashboardOverview.as_view(),
        name="dashboard_api_overview",
    ),

    # this line should be last value in urlpatterns
    path(r"<path:path>", ViewDashboardIndex.as_view(), name="dashboard_pages"),
]
