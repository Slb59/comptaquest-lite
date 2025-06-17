from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from tests.factories.nomadeposition import NomadePositionFactory


class NomadePositionAdminTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin_user = User.objects.create_superuser(trigram="adm", email="admin@example.com", password="password")
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.position = NomadePositionFactory()

    def test_admin_export_csv(self):
        """Test l'export CSV depuis l'interface admin"""
        url = reverse("admin:nomades_nomadeposition_changelist")
        data = {
            "action": "export_to_csv",
            "_selected_action": [self.position.id],
        }
        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
