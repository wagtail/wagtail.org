from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet, ModelViewSetGroup

from wagtailio.taxonomy.models import Category


class CategoryModelViewSet(ModelViewSet):
    model = Category
    icon = "tag"
    exclude_form_fields = []


class TaxonomiesModelViewSetGroup(ModelViewSetGroup):
    menu_label = "Taxonomy"
    menu_icon = "folder-inverse"
    items = (CategoryModelViewSet,)


@hooks.register("register_admin_viewset")
def register_taxonomy_viewsets():
    return TaxonomiesModelViewSetGroup()
