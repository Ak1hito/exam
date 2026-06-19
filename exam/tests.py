from django.test import TestCase
from django.urls import reverse


class PingTests(TestCase):
    def test_ping_returns_200(self):
        response = self.client.get(reverse("ping"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pong")
