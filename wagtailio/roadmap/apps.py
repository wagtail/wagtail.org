from django.apps import AppConfig, apps


class RoadmapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtailio.roadmap"

    def ready(self):
        if apps.is_installed("wagtail.api.v3"):
            from wagtail.api.v3.urls import api

            from wagtailio.roadmap.api import router

            api.add_router("/roadmap/", router)
