import copy
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail.models import APIToken

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
    return mock.patch("wagtailio.roadmap.sync.requests.post", return_value=response)


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
