from django.http import HttpRequest

from wagtail.api.v3.auth import BearerTokenAuth
from wagtail.api.v3.permissions import require_any_permission

from ninja import Router, Schema
from ninja.errors import HttpError

from wagtailio.roadmap.models import Milestone
from wagtailio.roadmap.sync import MissingTokenError, RoadmapSyncError, process


router = Router(tags=["roadmap"], auth=BearerTokenAuth())


class RoadmapSyncInputSchema(Schema):
    github_token: str = ""


class RoadmapSyncResultSchema(Schema):
    milestones: int
    items: int
    deleted_items: int


@router.post(
    "/sync/",
    response=RoadmapSyncResultSchema,
    url_name="roadmap_sync",
    operation_id="roadmap_sync",
    summary="Synchronise roadmap from GitHub",
    description=(
        "Fetch open milestones and their issues from the wagtail/roadmap GitHub "
        "repository and update the roadmap milestone snippets. If `github_token` "
        "is omitted, the server's configured token is used."
    ),
)
@require_any_permission(Milestone, ("add", "change"))
def sync_roadmap(request: HttpRequest, data: RoadmapSyncInputSchema | None = None):
    try:
        return process(token=data.github_token if data else "")
    except MissingTokenError as e:
        raise HttpError(422, str(e)) from e
    except RoadmapSyncError as e:
        raise HttpError(502, str(e)) from e
