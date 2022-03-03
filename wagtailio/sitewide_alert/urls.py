from django.urls import path

from . import views

app_name = "sitewide_alert"

urlpatterns = [path("", views.sitewide_alert, name="sitewide_alert")]
