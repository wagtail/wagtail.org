from django.conf.urls import url

from .views.view_main import ViewDashboardMain

urlpatterns = [
    url(r"^$", ViewDashboardMain.as_view(), name="dashboard_main"),
]
