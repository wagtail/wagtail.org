from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from wagtailio.taxonomy.models import Category


class CategoryModelAdmin(ModelAdmin):
    model = Category
    menu_icon = "tag"


class TaxonomiesModelAdminGroup(ModelAdminGroup):
    menu_label = "Taxonomy"
    items = (CategoryModelAdmin,)
    menu_icon = "folder-inverse"


modeladmin_register(TaxonomiesModelAdminGroup)
