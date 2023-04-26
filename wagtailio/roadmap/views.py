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

        for issue in node["issues"]["nodes"]:
            labels = {label["name"] for label in issue["labels"]["nodes"]}
            item = Item.objects.filter(number=issue["number"]).first()
            if not item:
                item = Item(number=issue["number"])

            item.state = issue["state"]
            item.title = issue["title"]
            item.url = issue["url"]
            item.milestone = milestone
            item.labels = ",".join(labels)
            item.full_clean()
            item.save()


class ImportView(TemplateView):
    template_name = "roadmap/import.html"

    def post(self, request):
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
