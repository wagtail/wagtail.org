from django.forms import ValidationError

from wagtail.admin.forms import WagtailAdminModelForm


class MainMenuSnippetForm(WagtailAdminModelForm):
    def clean(self):
        cleaned_data = super().clean()

        seen = []

        for form in self.formsets["menu_items"].forms:

            if form.is_valid():
                cleaned_form_data = form.clean()
                menu_item = cleaned_form_data.get("menu_item")
                menu_item_pk = menu_item.pk
                duplicates = [
                    menu_item for menu_item in seen if menu_item == menu_item_pk
                ]
                if duplicates:
                    for _ in duplicates:
                        form.add_error(
                            "menu_item",
                            ValidationError(
                                ("Duplicate menu items are not allowed"),
                                code="invalid",
                            ),
                        )

                else:
                    seen.append(menu_item_pk)

        return cleaned_data
