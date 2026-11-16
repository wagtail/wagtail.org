"""
Synchronise the roadmap from GitHub to wagtail.org through the Wagtail API.

Unlike ``wagtailio.roadmap.sync``, this runs outside of the Django project:
it fetches the roadmap from GitHub, then writes it to Wagtail using the
generic snippets API for the ``roadmap.Milestone`` snippet. The server never
talks to GitHub.

Usage::

    GITHUB_TOKEN=... WAGTAIL_API_TOKEN=... \\
        python -m wagtailio.roadmap.client https://wagtail.org/api/v3-preview/
"""

import argparse
import os
import sys
from typing import Any

import requests

from wagtailio.roadmap import github
from wagtailio.roadmap.github import RoadmapSyncError


WAGTAIL_REQUEST_TIMEOUT = 30
PAGE_SIZE = 20  # WAGTAILAPI_LIMIT_MAX


class RoadmapAPIClient:
    """
    Write roadmap milestones to the Wagtail snippets API.

    The snippets API identifies milestones and items by their Wagtail ID, and a
    PATCH with ``items`` replaces all of a milestone's items. To match the
    server-side sync, the client:

    - matches milestones and items by their GitHub number,
    - keeps each item's call to action URL (``cta_url``), which is not stored on
      GitHub, and its position as ordered by editors (new items go last),
    - removes items that have moved to another milestone from their old
      milestone first, as item numbers are unique,
    - leaves milestones that are no longer open on GitHub untouched.

    ``session`` only needs a ``requests.Session``-like ``request()`` method.
    """

    def __init__(self, api_url: str, token: str, session=None):
        self.url = f"{api_url.rstrip('/')}/snippets/roadmap.Milestone/"
        self.session = session or requests.Session()
        self.headers = {"Authorization": f"Bearer {token}"}

    def request(self, method: str, url: str, **kwargs) -> Any:
        try:
            response = self.session.request(
                method,
                url,
                headers=self.headers,
                timeout=WAGTAIL_REQUEST_TIMEOUT,
                **kwargs,
            )
        except requests.RequestException as e:
            raise RoadmapSyncError(f"Unable to reach the Wagtail API: {e}") from e

        if response.status_code >= 400:
            raise RoadmapSyncError(
                f"{method} {url} failed with {response.status_code}: {response.text}"
            )
        return response.json() if response.content else None

    def list_milestones(self) -> list[dict]:
        milestones = []
        while True:
            page = self.request(
                "GET",
                self.url,
                params={"limit": PAGE_SIZE, "offset": len(milestones)},
            )
            milestones.extend(page["items"])
            if not page["items"] or len(milestones) >= page["count"]:
                return milestones

    def save_milestone(self, milestone: dict, data: dict) -> dict:
        if milestone is None:
            return self.request("POST", self.url, json=data)
        return self.request("PATCH", f"{self.url}{milestone['id']}/", json=data)

    def sync(self, milestones: list[github.Milestone]) -> dict:
        existing = {
            milestone["number"]: milestone for milestone in self.list_milestones()
        }
        existing_items = {
            item["number"]: item
            for milestone in existing.values()
            for item in milestone["items"]
        }
        target_milestone_by_item = {
            item.number: milestone.number
            for milestone in milestones
            for item in milestone.items
        }

        # Remove items that have moved to another milestone from their current
        # milestone first, otherwise adding them to the new one fails because
        # their numbers are unique.
        for number, milestone in existing.items():
            remaining = [
                item
                for item in milestone["items"]
                if target_milestone_by_item.get(item["number"], number) == number
            ]
            if len(remaining) < len(milestone["items"]):
                existing[number] = self.save_milestone(
                    milestone, {"items": [as_input(item) for item in remaining]}
                )

        deleted_items = 0
        for data in milestones:
            milestone = existing.get(data.number)
            current_items = milestone["items"] if milestone else []
            github_items = {item.number: item for item in data.items}

            # Keep the current order of existing items, as editors may have
            # reordered them. Items not on GitHub anymore are left out, which
            # deletes them.
            items = []
            for item in current_items:
                github_item = github_items.pop(item["number"], None)
                if github_item:
                    items.append(
                        {**as_input(item), **github_item.model_dump(mode="json")}
                    )
                else:
                    deleted_items += 1

            # Append new items, carrying over the call to action URL of items
            # that have moved from another milestone.
            for number, github_item in github_items.items():
                cta_url = existing_items.get(number, {}).get("cta_url", "")
                items.append(
                    {**github_item.model_dump(mode="json"), "cta_url": cta_url}
                )

            self.save_milestone(
                milestone,
                {**data.model_dump(mode="json", exclude={"items"}), "items": items},
            )

        return {
            "milestones": len(milestones),
            "items": len(target_milestone_by_item),
            "deleted_items": deleted_items,
        }


def as_input(item: dict) -> dict:
    """Turn an item from an API response into input for a PATCH request."""
    return {key: value for key, value in item.items() if key != "meta"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[1])
    parser.add_argument(
        "api_url",
        help="Base URL of the Wagtail API, e.g. https://wagtail.org/api/v3-preview/",
    )
    args = parser.parse_args(argv)

    github_token = os.environ.get("GITHUB_TOKEN")
    wagtail_token = os.environ.get("WAGTAIL_API_TOKEN")
    if not github_token or not wagtail_token:
        parser.error("GITHUB_TOKEN and WAGTAIL_API_TOKEN must be set.")

    try:
        milestones = github.fetch(github_token)
        result = RoadmapAPIClient(args.api_url, wagtail_token).sync(milestones)
    except RoadmapSyncError as e:
        sys.exit(str(e))

    print(  # noqa: T201
        "Synchronised {milestones} milestones and {items} items, "
        "deleted {deleted_items} items.".format(**result)
    )


if __name__ == "__main__":
    main()
