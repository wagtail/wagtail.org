"""
Fetch the roadmap from the wagtail/roadmap GitHub repository.

This module must not depend on Django, so that it can be shared between the
server-side sync (``wagtailio.roadmap.sync``) and the API client
(``wagtailio.roadmap.client``), which runs outside of the Django project.

The schemas below validate GitHub's GraphQL response, and serialise
(with ``model_dump(mode="json")``) to the shape accepted by the Wagtail API
for the ``roadmap.Milestone`` snippet.
"""

import datetime
from typing import Annotated, Literal

from pydantic import AliasPath, BaseModel, BeforeValidator, Field, ValidationError
import requests


GITHUB_GRAPHQL_API_URL = "https://api.github.com/graphql"
GITHUB_REQUEST_TIMEOUT = 30

milestones_query = """
    {
        nodes {
        number
        state
        title
        url
        dueOn
        issues(first: 100) {
            nodes {
            number
            state
            title
            url
            labels(first: 10, orderBy: {field: NAME, direction: ASC}) {
                nodes {
                name
                }
            }
            }
        }
        }
    }
"""

graphql_query = {
    "query": f"""
        query {{
          repository(owner: "wagtail", name: "roadmap") {{

            # "Future" milestone has no due date, fetch separately because
            # null values are sorted last in descending order.
            future: milestones(
              first: 1
              states: [OPEN]
              query: "Future"
            ) {milestones_query}

            # Version milestones, sort by due date descending so that the most recent
            # versions are always retrieved when we have more than 20 open milestones.
            versions: milestones(
              first: 20
              states: [OPEN]
              orderBy: {{field: DUE_DATE, direction: DESC}}
              query: "v"
            ) {milestones_query}
          }}
        }}
    """,
    "variables": {},
}


class RoadmapSyncError(ValueError):
    pass


def _parse_due_on(value: str | None) -> datetime.date | None:
    # GitHub returns a datetime (e.g. "2027-02-01T08:00:00Z"), we only need the date.
    return datetime.datetime.fromisoformat(value).date() if value else None


def _join_labels(nodes: list[dict]) -> str:
    # Stored as a comma-separated string, see MilestoneItem.labels.
    return ",".join(sorted({node["name"] for node in nodes}))


State = Literal["OPEN", "CLOSED"]


class MilestoneItem(BaseModel):
    number: int
    state: State
    title: str
    url: str
    labels: Annotated[str, BeforeValidator(_join_labels)] = Field(
        validation_alias=AliasPath("labels", "nodes")
    )


class Milestone(BaseModel):
    number: int
    state: State
    due_on: Annotated[datetime.date | None, BeforeValidator(_parse_due_on)] = Field(
        validation_alias="dueOn"
    )
    title: str
    url: str
    items: list[MilestoneItem] = Field(validation_alias=AliasPath("issues", "nodes"))


class Repository(BaseModel):
    future: list[Milestone] = Field(validation_alias=AliasPath("future", "nodes"))
    versions: list[Milestone] = Field(validation_alias=AliasPath("versions", "nodes"))

    @property
    def milestones(self) -> list[Milestone]:
        return self.future + self.versions


def fetch(token: str) -> list[Milestone]:
    """Fetch the open roadmap milestones and their items from GitHub."""
    try:
        response = requests.post(
            GITHUB_GRAPHQL_API_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            json=graphql_query,
            timeout=GITHUB_REQUEST_TIMEOUT,
        )
        data = response.json().get("data")
    except (requests.RequestException, ValueError) as e:
        raise RoadmapSyncError(f"Unable to import data from GitHub: {e}") from e

    if not data:
        raise RoadmapSyncError(
            "Unable to import data from GitHub. Make sure the token is valid."
        )

    try:
        return Repository.model_validate(data["repository"]).milestones
    except (KeyError, TypeError, ValidationError) as e:
        raise RoadmapSyncError(f"Unexpected data from GitHub: {e}") from e
