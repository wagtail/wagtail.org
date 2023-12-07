from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup

from wagtailio.taxonomy.models import Category


class CategoryModelAdmin(ModelViewSet):
    model = Category
    icon = "tag"
    exclude_form_fields = []


class TaxonomiesAdminGroup(ModelViewSetGroup):
    menu_label = "Taxonomy"
    menu_icon = "folder-inverse"
    items = (CategoryModelAdmin,)


@hooks.register("register_admin_viewset")
def register_taxonomy_viewsets():
    return TaxonomiesAdminGroup()
