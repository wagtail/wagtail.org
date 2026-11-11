from django.conf import settings
from django.db import transaction
from django.utils.dateparse import parse_datetime

import requests

from wagtailio.roadmap.models import Milestone, MilestoneItem


GITHUB_API_HOST = "https://api.github.com"
GITHUB_GRAPHQL_API_URL = f"{GITHUB_API_HOST}/graphql"
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


class MissingTokenError(RoadmapSyncError):
    pass


def fetch(token):
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
    return data


def process(token=""):
    """
    Synchronise roadmap milestones and items from GitHub.

    Returns a summary dict with the number of milestones and items synchronised,
    and the number of stale items deleted.
    """
    token = token or settings.GITHUB_ROADMAP_ACCESS_TOKEN
    if not token:
        raise MissingTokenError("No GitHub access token supplied or configured.")

    data = fetch(token)

    repo = data["repository"]
    milestone_nodes = repo["future"]["nodes"] + repo["versions"]["nodes"]
    seen_milestone_numbers = set()
    seen_item_numbers = set()

    with transaction.atomic():
        for node in milestone_nodes:
            due_on = parse_datetime(node["dueOn"]).date() if node["dueOn"] else None
            milestone, _ = Milestone.objects.update_or_create(
                number=node["number"],
                defaults={
                    "state": node["state"],
                    "due_on": due_on,
                    "title": node["title"],
                    "url": node["url"],
                },
            )
            seen_milestone_numbers.add(node["number"])

            for issue in node["issues"]["nodes"]:
                labels = {label["name"] for label in issue["labels"]["nodes"]}
                item = MilestoneItem.objects.filter(number=issue["number"]).first()
                if not item:
                    item = MilestoneItem(number=issue["number"])
                seen_item_numbers.add(issue["number"])

                item.state = issue["state"]
                item.title = issue["title"]
                item.url = issue["url"]
                item.milestone = milestone
                item.labels = ",".join(labels)
                item.full_clean()
                item.save()

        # Remove items that are no longer attached to the seen milestones.
        deleted_items, _ = (
            MilestoneItem.objects.filter(milestone__number__in=seen_milestone_numbers)
            .exclude(number__in=seen_item_numbers)
            .delete()
        )

    return {
        "milestones": len(seen_milestone_numbers),
        "items": len(seen_item_numbers),
        "deleted_items": deleted_items,
    }
