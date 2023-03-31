from django.conf.urls import url
from django.urls import path

from .views.view_main import ViewDashboardIndex

urlpatterns = [
    url(r"^$", ViewDashboardIndex.as_view(), name="dashboard_main"),
    path(r"<path:path>", ViewDashboardIndex.as_view(), name="dashboard_pages"),
]
