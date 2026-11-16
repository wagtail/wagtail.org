import copy
import datetime
from json import dumps
from unittest import mock
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.models import APIToken

from wagtailio.roadmap import github, sync
from wagtailio.roadmap.client import RoadmapAPIClient
from wagtailio.roadmap.github import RoadmapSyncError
from wagtailio.roadmap.models import Milestone, MilestoneItem, State


def issue(number, title, labels=()):
    return {
        "number": number,
        "state": "OPEN",
        "title": title,
        "url": f"https://github.com/wagtail/roadmap/issues/{number}",
        "labels": {"nodes": [{"name": label} for label in labels]},
    }


def milestone(number, title, due_on, issues):
    return {
        "number": number,
        "state": "OPEN",
        "title": title,
        "url": f"https://github.com/wagtail/roadmap/milestone/{number}",
        "dueOn": due_on,
        "issues": {"nodes": issues},
    }


GITHUB_DATA = {
    "data": {
        "repository": {
            "future": {
                "nodes": [
                    milestone(1, "Future", None, [issue(10, "Some day")]),
                ]
            },
            "versions": {
                "nodes": [
                    milestone(
                        2,
                        "v8.2",
                        "2027-02-01T00:00:00Z",
                        [
                            issue(20, "Feature A", ["needs sponsorship"]),
                            issue(21, "Feature B", ["sponsored", "api"]),
                        ],
                    ),
                ]
            },
        }
    }
}


def mock_github(payload):
    response = mock.Mock()
    response.json.return_value = payload
    return mock.patch("wagtailio.roadmap.github.requests.post", return_value=response)


@override_settings(GITHUB_ROADMAP_ACCESS_TOKEN="settings-token")
class RoadmapSyncAPITest(TestCase):
    url = "/api/v3-preview/roadmap/sync/"

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        cls.editor = User.objects.create_user(
            username="editor", email="editor@example.com", password="password"
        )
        cls.editor.user_permissions.add(Permission.objects.get(codename="access_admin"))

    def authorize(self, user):
        _, plaintext = APIToken.create_token(user=user, name="test")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {plaintext}"

    def post(self, data=""):
        # An empty string sends an empty body, like `curl -X POST` with no data.
        return self.client.post(self.url, data, content_type="application/json")

    def test_sync(self):
        self.authorize(self.superuser)
        with mock_github(GITHUB_DATA) as post:
            response = self.post()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"milestones": 2, "items": 3, "deleted_items": 0}
        )
        self.assertEqual(
            post.call_args.kwargs["headers"]["Authorization"],
            "Bearer settings-token",
        )
        self.assertEqual(Milestone.objects.count(), 2)
        self.assertEqual(MilestoneItem.objects.count(), 3)
        item = MilestoneItem.objects.get(number=21)
        self.assertEqual(item.milestone.number, 2)
        self.assertEqual(item.state, State.OPEN)
        self.assertEqual(item.labels_set, {"sponsored", "api"})

    def test_sync_with_empty_body(self):
        self.authorize(self.superuser)
        with mock_github(GITHUB_DATA):
            response = self.post({})
        self.assertEqual(response.status_code, 200)

    def test_sync_removes_stale_items(self):
        self.authorize(self.superuser)
        with mock_github(GITHUB_DATA):
            self.post()

        payload = copy.deepcopy(GITHUB_DATA)
        payload["data"]["repository"]["versions"]["nodes"][0]["issues"]["nodes"].pop()
        with mock_github(payload):
            response = self.post()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"milestones": 2, "items": 2, "deleted_items": 1}
        )
        self.assertFalse(MilestoneItem.objects.filter(number=21).exists())

    def test_github_token_in_body_overrides_settings(self):
        self.authorize(self.superuser)
        with mock_github(GITHUB_DATA) as post:
            response = self.post({"github_token": "body-token"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            post.call_args.kwargs["headers"]["Authorization"], "Bearer body-token"
        )

    @override_settings(GITHUB_ROADMAP_ACCESS_TOKEN="")
    def test_missing_github_token(self):
        self.authorize(self.superuser)
        with mock_github(GITHUB_DATA) as post:
            response = self.post()

        self.assertEqual(response.status_code, 422)
        post.assert_not_called()

    def test_github_error(self):
        self.authorize(self.superuser)
        with mock_github({"message": "Bad credentials"}):
            response = self.post()

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response["Content-Type"], "application/problem+json")
        self.assertIn("Make sure the token is valid", response.json()["detail"])
        self.assertFalse(Milestone.objects.exists())

    def test_unauthenticated(self):
        with mock_github(GITHUB_DATA) as post:
            response = self.post()

        self.assertEqual(response.status_code, 401)
        post.assert_not_called()

    def test_session_auth_not_accepted(self):
        self.client.force_login(self.superuser)
        with mock_github(GITHUB_DATA) as post:
            response = self.post()

        self.assertEqual(response.status_code, 401)
        post.assert_not_called()

    def test_permission_denied(self):
        self.authorize(self.editor)
        with mock_github(GITHUB_DATA) as post:
            response = self.post()

        self.assertEqual(response.status_code, 403)
        post.assert_not_called()

    def test_change_permission_allowed(self):
        group = Group.objects.create(name="Roadmap editors")
        group.permissions.add(Permission.objects.get(codename="change_milestone"))
        self.editor.groups.add(group)
        self.authorize(self.editor)
        with mock_github(GITHUB_DATA):
            response = self.post()

        self.assertEqual(response.status_code, 200)


def api_item(number, title, labels=()):
    """A milestone item in the shape accepted by the snippets API."""
    return {
        "number": number,
        "state": "OPEN",
        "title": title,
        "url": f"https://github.com/wagtail/roadmap/issues/{number}",
        "labels": ",".join(labels),
    }


class MilestoneSnippetAPITest(TestCase):
    url = "/api/v3-preview/snippets/roadmap.Milestone/"

    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        cls.milestone = Milestone.objects.create(
            number=2,
            state=State.OPEN,
            due_on=datetime.date(2027, 2, 1),
            title="v8.2",
            url="https://github.com/wagtail/roadmap/milestone/2",
        )
        cls.item_a = MilestoneItem.objects.create(
            number=20,
            state=State.OPEN,
            title="Feature A",
            url="https://github.com/wagtail/roadmap/issues/20",
            labels="needs sponsorship",
            cta_url="https://example.com/sponsor",
            milestone=cls.milestone,
            sort_order=0,
        )
        cls.item_b = MilestoneItem.objects.create(
            number=21,
            state=State.OPEN,
            title="Feature B",
            url="https://github.com/wagtail/roadmap/issues/21",
            milestone=cls.milestone,
            sort_order=1,
        )

    def setUp(self):
        _, plaintext = APIToken.create_token(user=self.superuser, name="test")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {plaintext}"

    def post(self, data):
        return self.client.post(self.url, data, content_type="application/json")

    def patch(self, milestone, data):
        return self.client.patch(
            f"{self.url}{milestone.pk}/", data, content_type="application/json"
        )

    def test_detail(self):
        response = self.client.get(f"{self.url}{self.milestone.pk}/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["number"], 2)
        self.assertEqual(data["state"], "OPEN")
        self.assertEqual(data["due_on"], "2027-02-01")
        self.assertEqual(data["title"], "v8.2")
        self.assertEqual(data["display_title"], "February 2027")
        self.assertEqual(data["display_subtitle"], "v8.2")
        self.assertEqual(
            [(item["id"], item["number"]) for item in data["items"]],
            [(self.item_a.pk, 20), (self.item_b.pk, 21)],
        )
        self.assertEqual(data["items"][0]["labels"], "needs sponsorship")
        self.assertEqual(data["items"][0]["cta_url"], "https://example.com/sponsor")

    def test_create(self):
        response = self.post(
            {
                "number": 3,
                "state": "OPEN",
                "due_on": "2027-05-01",
                "title": "v8.3",
                "url": "https://github.com/wagtail/roadmap/milestone/3",
                "items": [
                    api_item(31, "Feature D", ["sponsored", "api"]),
                    api_item(30, "Feature C"),
                ],
            }
        )

        self.assertEqual(response.status_code, 201, response.content)
        milestone = Milestone.objects.get(number=3)
        self.assertEqual(response.json()["id"], milestone.pk)
        self.assertEqual(milestone.state, State.OPEN)
        self.assertEqual(milestone.due_on, datetime.date(2027, 5, 1))
        self.assertEqual(milestone.title, "v8.3")
        items = list(milestone.items.order_by("sort_order"))
        self.assertEqual([item.number for item in items], [31, 30])
        self.assertEqual(items[0].title, "Feature D")
        self.assertEqual(items[0].labels_set, {"sponsored", "api"})

    def test_create_future_milestone_without_due_date(self):
        response = self.post(
            {
                "number": 1,
                "state": "OPEN",
                "title": "Future",
                "url": "https://github.com/wagtail/roadmap/milestone/1",
            }
        )

        self.assertEqual(response.status_code, 201, response.content)
        milestone = Milestone.objects.get(number=1)
        self.assertIsNone(milestone.due_on)
        self.assertEqual(response.json()["display_title"], "Future")

    def test_create_duplicate_number(self):
        response = self.post(
            {
                "number": 2,
                "state": "OPEN",
                "title": "v8.2",
                "url": "https://github.com/wagtail/roadmap/milestone/2",
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(Milestone.objects.count(), 1)

    def test_update(self):
        response = self.patch(
            self.milestone,
            {
                "state": "CLOSED",
                "title": "v8.2 LTS",
                "items": [
                    # Reordered, updated, existing item B
                    {
                        "id": self.item_b.pk,
                        **api_item(21, "Feature B (renamed)", ["api"]),
                    },
                    # New item
                    api_item(22, "Feature E"),
                    # Item A is left out, so it is deleted
                ],
            },
        )

        self.assertEqual(response.status_code, 200, response.content)
        self.milestone.refresh_from_db()
        self.assertEqual(self.milestone.state, State.CLOSED)
        self.assertEqual(self.milestone.title, "v8.2 LTS")
        # Fields not submitted are left untouched
        self.assertEqual(self.milestone.due_on, datetime.date(2027, 2, 1))

        items = list(self.milestone.items.order_by("sort_order"))
        self.assertEqual([item.number for item in items], [21, 22])
        self.assertEqual(items[0].pk, self.item_b.pk)
        self.assertEqual(items[0].title, "Feature B (renamed)")
        self.assertEqual(items[0].labels_set, {"api"})
        self.assertFalse(MilestoneItem.objects.filter(number=20).exists())

    def test_update_without_items_keeps_items(self):
        response = self.patch(self.milestone, {"title": "v8.2 LTS"})

        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.milestone.items.count(), 2)

    def test_duplicate_item_number(self):
        other = Milestone.objects.create(
            number=3,
            state=State.OPEN,
            title="v8.3",
            url="https://github.com/wagtail/roadmap/milestone/3",
        )

        # Item 20 still belongs to the v8.2 milestone, so it must be removed
        # from there before it can be added to another milestone.
        response = self.patch(other, {"items": [api_item(20, "Feature A")]})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(self.item_a.milestone, self.milestone)
        self.assertFalse(other.items.exists())

    def test_delete(self):
        response = self.client.delete(f"{self.url}{self.milestone.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Milestone.objects.exists())
        self.assertFalse(MilestoneItem.objects.exists())


def github_milestones(payload=GITHUB_DATA):
    return github.Repository.model_validate(payload["data"]["repository"]).milestones


class GitHubSchemaTest(TestCase):
    def test_dump_as_api_input(self):
        payload = copy.deepcopy(GITHUB_DATA)
        payload["data"]["repository"]["versions"]["nodes"][0]["dueOn"] = (
            "2027-02-01T08:00:00Z"
        )
        future, version = github_milestones(payload)

        self.assertIsNone(future.due_on)
        self.assertEqual(
            version.model_dump(mode="json"),
            {
                "number": 2,
                "state": "OPEN",
                "due_on": "2027-02-01",
                "title": "v8.2",
                "url": "https://github.com/wagtail/roadmap/milestone/2",
                "items": [
                    api_item(20, "Feature A", ["needs sponsorship"]),
                    api_item(21, "Feature B", ["api", "sponsored"]),
                ],
            },
        )

    def test_unexpected_data(self):
        with (
            mock_github({"data": {"repository": {"future": None}}}),
            self.assertRaisesMessage(RoadmapSyncError, "Unexpected data from GitHub"),
        ):
            github.fetch("token")


class DjangoTestSession:
    """Route the API client's requests through the Django test client."""

    def __init__(self, client):
        self.client = client

    def request(self, method, url, headers=None, timeout=None, params=None, json=None):
        if params:
            url = f"{url}?{urlencode(params)}"
        response = self.client.generic(
            method,
            url,
            data=dumps(json) if json is not None else "",
            content_type="application/json",
            headers=headers,
        )
        response.text = response.content.decode()
        return response


class RoadmapAPIClientTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

    def setUp(self):
        _, plaintext = APIToken.create_token(user=self.superuser, name="test")
        self.api_client = RoadmapAPIClient(
            "/api/v3-preview/", plaintext, session=DjangoTestSession(self.client)
        )

    def snapshot(self):
        return [
            (
                milestone.number,
                milestone.state,
                milestone.due_on,
                milestone.title,
                milestone.url,
                [
                    (
                        item.number,
                        item.state,
                        item.title,
                        item.url,
                        item.labels,
                        item.cta_url,
                    )
                    for item in milestone.items.order_by("sort_order")
                ],
            )
            for milestone in Milestone.objects.order_by("number")
        ]

    def test_initial_sync_matches_server_sync(self):
        result = self.api_client.sync(github_milestones())

        self.assertEqual(result, {"milestones": 2, "items": 3, "deleted_items": 0})
        snapshot = self.snapshot()
        self.assertEqual(len(snapshot), 2)
        self.assertEqual([item[0] for item in snapshot[1][5]], [20, 21])

        MilestoneItem.objects.all().delete()
        Milestone.objects.all().delete()
        sync.apply(github_milestones())
        self.assertEqual(self.snapshot(), snapshot)

    def test_sync_keeps_editor_changes(self):
        self.api_client.sync(github_milestones())
        # Editors reorder items and set a call to action URL
        MilestoneItem.objects.filter(number=21).update(
            sort_order=0, cta_url="https://example.com/b"
        )
        MilestoneItem.objects.filter(number=20).update(sort_order=1)

        payload = copy.deepcopy(GITHUB_DATA)
        issues = payload["data"]["repository"]["versions"]["nodes"][0]["issues"][
            "nodes"
        ]
        issues[1]["title"] = "Feature B (renamed)"
        issues.append(issue(22, "Feature E"))
        result = self.api_client.sync(github_milestones(payload))

        self.assertEqual(result, {"milestones": 2, "items": 4, "deleted_items": 0})
        items = list(Milestone.objects.get(number=2).items.order_by("sort_order"))
        self.assertEqual([item.number for item in items], [21, 20, 22])
        self.assertEqual(items[0].title, "Feature B (renamed)")
        self.assertEqual(items[0].cta_url, "https://example.com/b")

    def test_sync_deletes_stale_items(self):
        self.api_client.sync(github_milestones())

        payload = copy.deepcopy(GITHUB_DATA)
        payload["data"]["repository"]["versions"]["nodes"][0]["issues"]["nodes"].pop()
        result = self.api_client.sync(github_milestones(payload))

        self.assertEqual(result, {"milestones": 2, "items": 2, "deleted_items": 1})
        self.assertFalse(MilestoneItem.objects.filter(number=21).exists())

    def test_sync_moves_items(self):
        self.api_client.sync(github_milestones())
        MilestoneItem.objects.filter(number=21).update(cta_url="https://example.com/b")

        payload = copy.deepcopy(GITHUB_DATA)
        repository = payload["data"]["repository"]
        moved = repository["versions"]["nodes"][0]["issues"]["nodes"].pop()
        repository["future"]["nodes"][0]["issues"]["nodes"].append(moved)
        result = self.api_client.sync(github_milestones(payload))

        self.assertEqual(result, {"milestones": 2, "items": 3, "deleted_items": 0})
        item = MilestoneItem.objects.get(number=21)
        self.assertEqual(item.milestone.number, 1)
        self.assertEqual(item.cta_url, "https://example.com/b")

    def test_list_milestones_paginates(self):
        Milestone.objects.bulk_create(
            Milestone(number=i, state=State.OPEN, title=f"v{i}", url=f"https://x/{i}")
            for i in range(25)
        )

        self.assertEqual(len(self.api_client.list_milestones()), 25)

    def test_api_error(self):
        self.api_client.headers = {"Authorization": "Bearer invalid"}

        with self.assertRaisesMessage(RoadmapSyncError, "failed with 401"):
            self.api_client.sync(github_milestones())


@override_settings(GITHUB_ROADMAP_ACCESS_TOKEN="settings-token")
class RoadmapImportViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

    def setUp(self):
        self.client.force_login(self.superuser)

    def test_import(self):
        with mock_github(GITHUB_DATA):
            response = self.client.post(
                reverse("roadmap:import"), {"github_token": "form-token"}, follow=True
            )

        self.assertContains(response, "Successfully updated roadmap data from GitHub.")
        self.assertEqual(MilestoneItem.objects.count(), 3)

    def test_import_error(self):
        with mock_github({}):
            response = self.client.post(
                reverse("roadmap:import"), {"github_token": "form-token"}, follow=True
            )

        self.assertContains(response, "Make sure the token is valid")
        self.assertFalse(Milestone.objects.exists())
