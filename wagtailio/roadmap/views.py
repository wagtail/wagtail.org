from django.conf import settings
from django.utils.dateparse import parse_datetime
import requests

from wagtailio.roadmap.models import Item, Milestone, State

GITHUB_API_HOST = "https://api.github.com"
GITHUB_GRAPHQL_API_URL = f"{GITHUB_API_HOST}/graphql"

graphql_query = {
    "query": """
        query {
          repository(owner: "wagtail", name: "roadmap") {
            milestones(first: 20, states: [OPEN], orderBy: {field: DUE_DATE, direction: ASC}) {
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
    """,
    "variables": {},
}

headers = {
    "Authorization": f"Bearer {settings.GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def process():
    response = requests.post(
        GITHUB_GRAPHQL_API_URL,
        headers=headers,
        json=graphql_query,
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
