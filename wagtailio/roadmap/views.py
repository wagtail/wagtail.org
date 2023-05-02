from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.views.generic import TemplateView

from wagtail.admin import messages

import requests

from wagtailio.roadmap.models import Milestone, MilestoneItem

GITHUB_API_HOST = "https://api.github.com"
GITHUB_GRAPHQL_API_URL = f"{GITHUB_API_HOST}/graphql"

milestones_query = """
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
"""

graphql_query = {
    "query": """
        query {
          repository(owner: "wagtail", name: "roadmap") {

            # "Future" milestone has no due date, fetch separately because
            # null values are sorted last in descending order.
            future: milestones(
              first: 1
              states: [OPEN]
              query: "Future"
            ) {
              %(milestones_query)s
            }

            # Version milestones, sort by due date descending so that the most recent
            # versions are always retrieved when we have more than 20 open milestones.
            versions: milestones(
              first: 20
              states: [OPEN]
              orderBy: {field: DUE_DATE, direction: DESC}
              query: "v"
            ) {
              %(milestones_query)s
            }

          }
        }
    """
    % {"milestones_query": milestones_query},
    "variables": {},
}

headers = {
    "Authorization": f"Bearer {settings.GITHUB_ROADMAP_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def process():
    response = requests.post(
        GITHUB_GRAPHQL_API_URL,
        headers=headers,
        json=graphql_query,
    )
    data = response.json()["data"]
    repo = data["repository"]
    milestone_nodes = repo["future"]["nodes"] + repo["versions"]["nodes"]
    seen_milestone_numbers = set()
    seen_item_numbers = set()

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
    (
        MilestoneItem.objects.filter(milestone__number__in=seen_milestone_numbers)
        .exclude(number__in=seen_item_numbers)
        .delete()
    )


class ImportView(TemplateView):
    template_name = "roadmap/import.html"

    def post(self, request):
        if not settings.GITHUB_ROADMAP_ACCESS_TOKEN:
            messages.error(
                request,
                "No GitHub access token set. Please set the GITHUB_ROADMAP_ACCESS_TOKEN "
                "environment variable.",
            )
            return redirect("roadmap:import")

        with transaction.atomic():
            process()

        messages.success(
            request,
            "Successfully updated roadmap data from GitHub.",
            buttons=[
                messages.button(
                    reverse("wagtailsnippets_roadmap_milestone:list"), "View"
                )
            ],
        )
        return redirect("roadmap:import")
