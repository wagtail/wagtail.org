from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from django.views.generic import TemplateView

from wagtail.admin import messages

import requests

from wagtailio.roadmap.models import Item, Milestone, State

GITHUB_API_HOST = "https://api.github.com"
GITHUB_GRAPHQL_API_URL = f"{GITHUB_API_HOST}/graphql"


def get_graphql_query():
    return """
        query RoadmapData($states: [MilestoneState!]) {
          repository(owner: "wagtail", name: "roadmap") {
            milestones(first: 20, states: $states, orderBy: {field: DUE_DATE, direction: ASC}) {
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
          }
        }
    """


headers = {
    "Authorization": f"Bearer {settings.GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def process(import_all=True):
    states = ["OPEN"]
    if import_all:
        states.append("CLOSED")

    response = requests.post(
        GITHUB_GRAPHQL_API_URL,
        headers=headers,
        json={
            "query": get_graphql_query(),
            "variables": {"states": states},
        },
    )
    data = response.json()["data"]
    milestone_nodes = data["repository"]["milestones"]["nodes"]
    seen_milestone_numbers = set()
    seen_item_numbers = set()

    for node in milestone_nodes:
        due_on = parse_datetime(node["dueOn"]).date() if node["dueOn"] else None
        milestone, _ = Milestone.objects.update_or_create(
            number=node["number"],
            defaults={
                "publish": node["state"] == State.OPEN,
                "state": node["state"],
                "due_on": due_on,
                "title": node["title"],
                "url": node["url"],
            },
        )
        seen_milestone_numbers.add(node["number"])

        for issue in node["issues"]["nodes"]:
            labels = {label["name"] for label in issue["labels"]["nodes"]}
            item = Item.objects.filter(number=issue["number"]).first()
            if not item:
                item = Item(number=issue["number"])
            seen_item_numbers.add(issue["number"])

            item.state = issue["state"]
            item.title = issue["title"]
            item.url = issue["url"]
            item.milestone = milestone
            item.labels = ",".join(labels)
            item.full_clean()
            item.save()

    # If importing all milestones, remove milestones that are not in the response.
    if import_all:
        Milestone.objects.exclude(number__in=seen_milestone_numbers).delete()

    # Remove items that are no longer attached to the seen milestones.
    (
        Item.objects.filter(milestone__number__in=seen_milestone_numbers)
        .exclude(number__in=seen_item_numbers)
        .delete()
    )


class ImportView(TemplateView):
    template_name = "roadmap/import.html"

    def post(self, request):
        if not settings.GITHUB_ACCESS_TOKEN:
            messages.error(
                request,
                "No GitHub access token set. Please set the GITHUB_ACCESS_TOKEN "
                "environment variable.",
            )
            return redirect("roadmap:import")

        import_all = "import-all" in request.POST
        with transaction.atomic():
            process(import_all=import_all)

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
