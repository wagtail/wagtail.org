from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.core.models import Page

from wagtailio.areweheadlessyet.models import AreWeHeadlessYetHomePage

api_router = WagtailAPIRouter("wagtailapi")


class AreWeHeadlessYetPagesAPIViewSet(PagesAPIViewSet):
    def get_base_queryset(self):
        """Returns a queryset containing only pages from the AreWeHeadLessYet site."""

        areweheadlessyet_queryset = AreWeHeadlessYetHomePage.objects.all()
        if not areweheadlessyet_queryset:
            return areweheadlessyet_queryset

        areweheadlessyet_root_page = areweheadlessyet_queryset[0]
        return Page.objects.live().descendant_of(
            areweheadlessyet_root_page, inclusive=True
        )


api_router.register_endpoint("pages", AreWeHeadlessYetPagesAPIViewSet)
