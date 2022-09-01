from django.forms import ValidationError

from wagtail.admin.forms import WagtailAdminModelForm


class MainMenuForm(WagtailAdminModelForm):
    def clean(self):
        cleaned_data = super().clean()

        seen = []

        for form in self.formsets["menu_sections"].forms:

            if form.is_valid():
                cleaned_form_data = form.clean()
                menu_section = cleaned_form_data.get("menu_section")
                menu_section_pk = menu_section.pk
                duplicates = [
                    menu_section
                    for menu_section in seen
                    if menu_section == menu_section_pk
                ]
                if duplicates:
                    for _ in duplicates:
                        form.add_error(
                            "menu_section",
                            ValidationError(
                                ("Duplicate menu sections are not allowed"),
                                code="invalid",
                            ),
                        )

                else:
                    seen.append(menu_section_pk)

        return cleaned_data
