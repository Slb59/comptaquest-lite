from django.test import Client, TestCase
from django.urls import reverse

from tests.factories.member import MemberFactory
from tests.factories.nomadeposition import NomadePositionFactory


class NomadePositionAdminTests(TestCase):
    def setUp(self):
        self.admin_user = MemberFactory(
            trigram="adm", 
            email="admin@example.com", 
            password="password",  # nosec: B106
            is_superuser=True, 
            is_staff=True
        )
        self.admin_user.save()
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.pos1 = NomadePositionFactory(name="Test 1", city="Paris")
        self.pos1.save()
        print(self.pos1.city)

    def test_admin_export_csv(self):
        """Test CSV export from the admin interface"""
        url = reverse("admin:escapevault_nomadeposition_changelist")
        data = {
            "action": "export_to_csv",
            "_selected_action": [self.pos1.id],
        }
        response = self.client.post(url, data, follow=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

        content = response.content.decode("utf-8")
        self.assertIn("Test 1", content)
        self.assertIn("Paris", content)
