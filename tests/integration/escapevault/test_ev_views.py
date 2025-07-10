from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from escapevault.models import NomadePosition
from tests.factories.member import MemberFactory
from tests.factories.nomadeposition import NomadePositionFactory

User = get_user_model()


class EscapeVaultViewsTests(TestCase):
    def setUp(self):
        self.user = MemberFactory()
        self.client.force_login(self.user)
        self.position = NomadePositionFactory()

    def test_map_view(self):
        response = self.client.get(reverse("escapevault:evmap"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("EscapeVault Map", response.content.decode())
        self.assertIn("<div", response.context["map"])

    def test_parameters_view(self):
        response = self.client.get(reverse("escapevault:parameters"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "EscapeVault Param")

    def test_create_view_get(self):
        response = self.client.get(reverse("escapevault:add_position"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nouvelle Position")

    def test_create_view_post(self):
        data = {
            "name": "Test Position",
            "category": "home",
            "city": "Paris",
            "country": self.position.country,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "stars": 4,
        }
        response = self.client.post(reverse("escapevault:add_position"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NomadePosition.objects.filter(name="Test Position").exists())

    def test_list_view(self):
        response = self.client.get(reverse("escapevault:list_positions"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_edit_view_get(self):
        url = reverse("escapevault:edit_position", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_edit_view_post_with_review(self):
        url = reverse("escapevault:edit_position", kwargs={"pk": self.position.pk})
        response = self.client.post(
            url,
            {
                "name": self.position.name,
                "category": self.position.category,
                "city": self.position.city,
                "country": self.position.country,
                "latitude": self.position.latitude,
                "longitude": self.position.longitude,
                "stars": self.position.stars,
                "new_review": "Avis test",
            },
        )
        if response.status_code == 200:
            print("Form errors:", response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertIn("Avis test", [r["text"] for r in self.position.reviews])

    def test_delete_view_get(self):
        url = reverse("escapevault:delete_position", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)

    def test_delete_view_post(self):
        url = reverse("escapevault:delete_position", kwargs={"pk": self.position.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(NomadePosition.objects.filter(pk=self.position.pk).exists())
