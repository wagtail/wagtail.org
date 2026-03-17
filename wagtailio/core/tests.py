from django.test import SimpleTestCase
from django.urls import reverse


class SecurityViewTestCase(SimpleTestCase):
    url = reverse("security-txt")

    def test_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Canonical: http://testserver/.well-known/security.txt"
        )
