from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response


@method_decorator(login_required, name="dispatch")
class ApiViewDashboardOverview(generics.GenericAPIView):
    def get(self, request):
        return Response(
            status=200,
            data={
                "test": {
                    "message": "received"
                }
            },
        )
