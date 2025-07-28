from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from tests.factories.member import MemberFactory


class EscapeVaultAccessTest(TestCase):
    def setUp(self):
        self.url = reverse("escapevault:evmap")

        # user with no group
        self.user_no_group = MemberFactory(email="user1@example.com", trigram="us1", password="pass")

        # user with group
        self.user_with_group = MemberFactory(email="user2@example.com", trigram="us2", password="pass")
        group = Group.objects.create(name="escapevault_access")
        self.user_with_group.groups.add(group)

        # superuser
        self.superuser = MemberFactory(trigram="adm", password="pass", email="admin@example.com", is_superuser=True)

    def test_access_denied_for_anonymous(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        # redirect login (302) or 403

    def test_access_denied_for_user_without_group(self):
        self.client.login(email="user1@example.com", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_for_user_with_group(self):
        self.client.login(email="user2@example.com", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_granted_for_superuser(self):
        self.client.login(email="admin@example.com", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
