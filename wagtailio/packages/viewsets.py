from wagtail.admin.ui.tables import BooleanColumn
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup

from .models import Grid, Package


class BaseModelViewSet(ModelViewSet):
    icon = "doc-full-inverse"
    list_display = [
        "title",
        BooleanColumn(
            "publish",
            sort_key="publish",
        ),
    ]
    list_filter = ["publish"]
    search_fields = ["title"]

    def on_register(self):
        super().on_register()
        # used in `get_admin_url` for the models
        self.model.model_viewset = self


class GridAdmin(BaseModelViewSet):
    model = Grid
    form_fields = ["publish", "title", "slug", "description"]


class PackageAdmin(BaseModelViewSet):
    model = Package
    form_fields = ["publish", "title", "slug", "repo_description"]


class PackagesAdminGroup(ModelViewSetGroup):
    menu_label = "Packages"
    menu_icon = "cube"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = [GridAdmin, PackageAdmin]
