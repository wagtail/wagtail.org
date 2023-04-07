from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name="dispatch")
class ViewDashboardIndex(View):
    template_name = "dashboard/index.html"

    # get request
    def get(self, request, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
        )
