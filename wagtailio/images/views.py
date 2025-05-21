from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField, Count, OuterRef, Subquery
from django.db.models.functions import Cast, Coalesce
from django.utils.translation import gettext_lazy as _

from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.reports import ReportView
from wagtail.models import ReferenceIndex

from .models import WagtailIOImage


class ImageUsageReport(ReportView):
    page_title = "Image usage report"
    header_icon = "image"
    index_url_name = "image_usage_report"
    index_results_url_name = "image_usage_report_results"
    default_ordering = "-usage_count"
    columns = [
        TitleColumn(
            "title",
            label=_("Image Title"),
            url_name="wagtailimages:edit",
            sort_key="title",
        ),
        TitleColumn(
            "usage_count",
            label=_("Times Used"),
            url_name="wagtailimages:image_usage",
            sort_key="usage_count",
        ),
    ]
    list_export = ["title", "description", "usage_count", "created_at"]
    export_headings = {
        "usage_count": _("Times Used"),
    }
    export_filename = "image_usage_report"

    def get_base_queryset(self):
        # Create the subquery to count matching ReferenceIndex rows
        reference_index_subquery = (
            ReferenceIndex.objects.filter(
                to_content_type=ContentType.objects.get_for_model(WagtailIOImage),
                # to_object_id is a varchar so we need to cast the image PK to a varchar for comparison
                to_object_id=Cast(OuterRef("pk"), output_field=CharField()),
            )
            .values("object_id", "to_object_id")
            .distinct()
            .values("to_object_id")
            .annotate(count=Count("object_id", distinct=True))
            .values("count")
        )

        return WagtailIOImage.objects.annotate(
            usage_count=Coalesce(Subquery(reference_index_subquery.values("count")), 0)
        )
