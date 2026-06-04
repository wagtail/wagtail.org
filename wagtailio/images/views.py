from django.contrib.contenttypes.models import ContentType
from django.db.models import CharField, Count, OuterRef, Subquery
from django.db.models.functions import Cast, Coalesce
from django.utils.translation import gettext_lazy as _

from wagtail.admin.filters import CollectionFilter, WagtailFilterSet
from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.reports import ReportView
from wagtail.models import Collection, ReferenceIndex

from django_filters import ChoiceFilter as DjangoChoiceFilter

from .models import WagtailIOImage


class UsageFilter(DjangoChoiceFilter):
    def filter(self, qs, value):
        # Value passed will be one of the choices
        if value:
            if value in ["0", "1"]:
                return qs.filter(usage_count=value)
            else:
                # If the value is not 0 or 1, we can assume means greater than 1
                return qs.filter(usage_count__gt=1)
        # If the value is not in the choices, return the original queryset
        return qs


class ImageUsageReportFilterSet(WagtailFilterSet):
    collection = CollectionFilter(
        label=_("Collection"),
        help_text=_("Filter images by their collection."),
    )
    usage = UsageFilter(
        label=_("Usage"),
        help_text=_("Filter images by their usage count."),
        choices=[
            (0, _("Not used")),
            (1, _("Used once")),
            (2, _("Used more than once")),
        ],
    )

    class Meta:
        model = WagtailIOImage
        fields = ["collection", "usage"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections = {
            collection.pk: collection for collection in Collection.objects.all()
        }
        self.collections_filter_enabled = True
        if len(self.collections) == 1:
            # If there is only one collection, we don't need to show the collection filter
            self.collections_filter_enabled = False
            del self.filters["collection"]


class ImageUsageReport(ReportView):
    page_title = "Image usage report"
    header_icon = "image"
    index_url_name = "image_usage_report"
    index_results_url_name = "image_usage_report_results"
    filterset_class = ImageUsageReportFilterSet
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
