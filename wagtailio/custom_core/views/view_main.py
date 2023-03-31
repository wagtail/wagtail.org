from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from wagtailio.custom_core.forms.form_empty import EmptyForm


@method_decorator(login_required, name='dispatch')
class ViewDashboardMain(View):
    form_class = EmptyForm
    template_name = "dashboard/index.html"

    # get request
    def get(self, request):
        form = self.form_class()

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )
